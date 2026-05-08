"""Analytical logic for anomaly detection and short-horizon forecasting."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import HuberRegressor, LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


class WeatherAnalytics:
    """Stateless analytical routines over normalized weather observations."""

    DEFAULT_METRICS = [
        "temp_c",
        "pressure_hpa",
        "humidity_pct",
        "wind_speed_kph",
        "precipitation_mm",
    ]

    def detect_anomalies(
        self,
        observations: pd.DataFrame,
        rolling_window: int = 8,
        z_threshold: float = 2.2,
    ) -> pd.DataFrame:
        """Detect weather outliers using prior rolling z-scores and hard deltas."""

        frame = self._prepare(observations)
        if frame.empty:
            return pd.DataFrame()

        anomaly_rows = []
        for metric in [metric for metric in self.DEFAULT_METRICS if metric in frame.columns]:
            values = pd.to_numeric(frame[metric], errors="coerce")
            baseline = values.shift(1).rolling(rolling_window, min_periods=3)
            rolling_mean = baseline.mean()
            rolling_std = baseline.std(ddof=0).replace(0, np.nan)
            z_scores = ((values - rolling_mean) / rolling_std).replace([np.inf, -np.inf], np.nan)

            for idx in frame.index[z_scores.abs() >= z_threshold]:
                anomaly_rows.append(
                    {
                        "observed_at": frame.at[idx, "observed_at"],
                        "source": frame.at[idx, "source"],
                        "metric": metric,
                        "value": values.at[idx],
                        "rolling_mean": rolling_mean.at[idx],
                        "z_score": z_scores.at[idx],
                        "severity": self._severity(z_scores.at[idx]),
                        "reason": f"{metric} deviated {z_scores.at[idx]:.2f} sigma from rolling baseline",
                    }
                )

        anomaly_rows.extend(self._detect_sudden_pressure_drops(frame))
        anomaly_rows.extend(self._detect_temperature_jumps(frame))

        if not anomaly_rows:
            return pd.DataFrame(
                columns=[
                    "observed_at",
                    "source",
                    "metric",
                    "value",
                    "rolling_mean",
                    "z_score",
                    "severity",
                    "reason",
                ]
            )

        return (
            pd.DataFrame(anomaly_rows)
            .sort_values(["observed_at", "severity"], ascending=[False, True])
            .drop_duplicates(["observed_at", "metric", "reason"])
            .reset_index(drop=True)
        )

    def forecast_next_6_hours(self, observations: pd.DataFrame) -> pd.DataFrame:
        """Forecast the next 6 hourly points from the current session cache."""

        frame = self._prepare(observations)
        if frame.empty:
            return pd.DataFrame()

        metrics = ["temp_c", "pressure_hpa", "humidity_pct", "wind_speed_kph"]
        prediction_times = pd.date_range(
            start=frame["observed_at"].max() + pd.Timedelta(hours=1),
            periods=6,
            freq="h",
        )
        predictions = pd.DataFrame({"forecast_at": prediction_times})

        for metric in metrics:
            if metric not in frame.columns:
                continue
            series_frame = frame[["observed_at", metric]].dropna()
            if len(series_frame) < 3:
                predictions[metric] = series_frame[metric].iloc[-1] if not series_frame.empty else np.nan
                predictions[f"{metric}_model"] = "persistence"
                continue

            x_train = self._time_features(series_frame["observed_at"], frame["observed_at"].min())
            y_train = series_frame[metric].astype(float)
            x_pred = self._time_features(prediction_times, frame["observed_at"].min())

            model = self._select_model(len(series_frame))
            model.fit(x_train, y_train)
            predictions[metric] = model.predict(x_pred)
            predictions[f"{metric}_model"] = model.__class__.__name__

        predictions["generated_at"] = pd.Timestamp.utcnow().tz_localize(None)
        predictions["confidence"] = self._confidence_label(len(frame))
        return predictions

    def summarize_operations(self, observations: pd.DataFrame, anomalies: pd.DataFrame) -> dict[str, float | int]:
        """Return compact operational metrics for dashboard KPIs."""

        frame = self._prepare(observations)
        if frame.empty:
            return {
                "records": 0,
                "temp_latest": np.nan,
                "pressure_latest": np.nan,
                "wind_latest": np.nan,
                "anomalies": 0,
            }

        latest = frame.iloc[-1]
        return {
            "records": int(len(frame)),
            "temp_latest": float(latest.get("temp_c", np.nan)),
            "pressure_latest": float(latest.get("pressure_hpa", np.nan)),
            "wind_latest": float(latest.get("wind_speed_kph", np.nan)),
            "anomalies": int(len(anomalies)),
        }

    def _prepare(self, observations: pd.DataFrame) -> pd.DataFrame:
        if observations is None or observations.empty:
            return pd.DataFrame()

        frame = observations.copy()
        frame["observed_at"] = pd.to_datetime(frame["observed_at"], errors="coerce")
        frame = frame.dropna(subset=["observed_at"]).sort_values("observed_at")
        frame = frame.drop_duplicates(["observed_at", "source"], keep="last").reset_index(drop=True)

        for metric in self.DEFAULT_METRICS:
            if metric in frame.columns:
                frame[metric] = pd.to_numeric(frame[metric], errors="coerce")

        return frame

    def _detect_sudden_pressure_drops(self, frame: pd.DataFrame) -> list[dict[str, object]]:
        if "pressure_hpa" not in frame.columns:
            return []

        rows = []
        pressure_delta = frame["pressure_hpa"].diff()
        for idx in frame.index[pressure_delta <= -4.0]:
            rows.append(
                {
                    "observed_at": frame.at[idx, "observed_at"],
                    "source": frame.at[idx, "source"],
                    "metric": "pressure_hpa",
                    "value": frame.at[idx, "pressure_hpa"],
                    "rolling_mean": np.nan,
                    "z_score": np.nan,
                    "severity": "high" if pressure_delta.at[idx] <= -7.0 else "medium",
                    "reason": f"pressure dropped {abs(pressure_delta.at[idx]):.1f} hPa between readings",
                }
            )
        return rows

    def _detect_temperature_jumps(self, frame: pd.DataFrame) -> list[dict[str, object]]:
        if "temp_c" not in frame.columns:
            return []

        rows = []
        temp_delta = frame["temp_c"].diff()
        for idx in frame.index[temp_delta.abs() >= 3.5]:
            direction = "spiked" if temp_delta.at[idx] > 0 else "dropped"
            rows.append(
                {
                    "observed_at": frame.at[idx, "observed_at"],
                    "source": frame.at[idx, "source"],
                    "metric": "temp_c",
                    "value": frame.at[idx, "temp_c"],
                    "rolling_mean": np.nan,
                    "z_score": np.nan,
                    "severity": "medium",
                    "reason": f"temperature {direction} {abs(temp_delta.at[idx]):.1f} C between readings",
                }
            )
        return rows

    @staticmethod
    def _time_features(times: pd.Series | pd.DatetimeIndex, origin: pd.Timestamp) -> np.ndarray:
        timestamps = pd.to_datetime(times)
        deltas = timestamps - pd.Timestamp(origin)
        if isinstance(deltas, pd.Series):
            hours = deltas.dt.total_seconds().to_numpy() / 3600.0
        else:
            hours = deltas.total_seconds() / 3600.0
        if isinstance(timestamps, pd.Series):
            hour_of_day = timestamps.dt.hour.to_numpy() + timestamps.dt.minute.to_numpy() / 60.0
        else:
            hour_of_day = timestamps.hour + timestamps.minute / 60.0
        return np.column_stack(
            [
                hours,
                np.square(hours),
                np.sin(2 * np.pi * hour_of_day / 24),
                np.cos(2 * np.pi * hour_of_day / 24),
            ]
        )

    @staticmethod
    def _select_model(row_count: int):
        if row_count >= 8:
            return make_pipeline(StandardScaler(), HuberRegressor(max_iter=500))
        return LinearRegression()

    @staticmethod
    def _confidence_label(row_count: int) -> str:
        if row_count >= 24:
            return "medium"
        if row_count >= 8:
            return "experimental"
        return "low"

    @staticmethod
    def _severity(z_score: float) -> str:
        magnitude = abs(z_score)
        if magnitude >= 3.5:
            return "critical"
        if magnitude >= 2.8:
            return "high"
        return "medium"
