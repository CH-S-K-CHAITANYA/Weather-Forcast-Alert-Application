"""Data acquisition and DuckDB persistence layer.

This module is intentionally UI-agnostic. It owns all network acquisition,
normalization, persistence, and analytical read queries.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd
import requests

from .config import Settings


BASE_URL = "https://api.openweathermap.org/data/2.5"


class WeatherAcquisitionError(RuntimeError):
    """Raised when live weather acquisition fails."""


@dataclass(frozen=True)
class WeatherSnapshot:
    """A complete weather acquisition result for one city."""

    city: str
    country: str
    latitude: float
    longitude: float
    current: pd.DataFrame
    forecast: pd.DataFrame
    combined: pd.DataFrame


class WeatherEngine:
    """Service object for acquiring, storing, and querying weather data."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.db_path = Path(settings.db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize_schema()

    def connect(self) -> duckdb.DuckDBPyConnection:
        """Open a DuckDB connection."""

        return duckdb.connect(str(self.db_path))

    def initialize_schema(self) -> None:
        """Create a small analytical warehouse schema."""

        with self.connect() as con:
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS locations (
                    location_id VARCHAR PRIMARY KEY,
                    city VARCHAR NOT NULL,
                    country VARCHAR,
                    latitude DOUBLE,
                    longitude DOUBLE,
                    first_seen_at TIMESTAMP,
                    last_seen_at TIMESTAMP
                )
                """
            )
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS weather_observations (
                    observation_id VARCHAR PRIMARY KEY,
                    location_id VARCHAR NOT NULL,
                    observed_at TIMESTAMP NOT NULL,
                    acquired_at TIMESTAMP NOT NULL,
                    source VARCHAR NOT NULL,
                    temp_c DOUBLE,
                    feels_like_c DOUBLE,
                    humidity_pct DOUBLE,
                    pressure_hpa DOUBLE,
                    wind_speed_kph DOUBLE,
                    wind_direction_deg DOUBLE,
                    cloud_cover_pct DOUBLE,
                    visibility_km DOUBLE,
                    precipitation_mm DOUBLE,
                    precipitation_probability_pct DOUBLE,
                    condition_id INTEGER,
                    description VARCHAR,
                    payload_json VARCHAR
                )
                """
            )
            con.execute(
                "CREATE INDEX IF NOT EXISTS idx_weather_location_time "
                "ON weather_observations(location_id, observed_at)"
            )
            con.execute(
                "CREATE INDEX IF NOT EXISTS idx_weather_source_time "
                "ON weather_observations(source, observed_at)"
            )

    def fetch_city_snapshot(self, city: str) -> WeatherSnapshot:
        """Fetch current and forecast data, normalize it, and persist it."""

        if not self.settings.api_key:
            raise WeatherAcquisitionError("WEATHER_API_KEY is missing. Add it to .env.")

        current_payload = self._request("weather", {"q": city})
        forecast_payload = self._request("forecast", {"q": city})

        acquired_at = datetime.now(timezone.utc)
        current = pd.DataFrame([self._parse_current(current_payload, acquired_at)])
        forecast = pd.DataFrame(self._parse_forecast(forecast_payload, acquired_at))
        combined = pd.concat([current, forecast], ignore_index=True)

        self.persist_observations(combined)

        first = combined.iloc[0]
        return WeatherSnapshot(
            city=str(first["city"]),
            country=str(first["country"]),
            latitude=float(first["latitude"]),
            longitude=float(first["longitude"]),
            current=current,
            forecast=forecast,
            combined=combined,
        )

    def persist_observations(self, observations: pd.DataFrame) -> int:
        """Persist normalized observations into DuckDB with deterministic ids."""

        if observations.empty:
            return 0

        frame = observations.copy()
        frame["location_id"] = frame.apply(self._location_id_from_row, axis=1)
        frame["observation_id"] = frame.apply(self._observation_id_from_row, axis=1)

        locations = (
            frame[
                [
                    "location_id",
                    "city",
                    "country",
                    "latitude",
                    "longitude",
                    "acquired_at",
                ]
            ]
            .drop_duplicates("location_id")
            .rename(columns={"acquired_at": "last_seen_at"})
        )
        locations["first_seen_at"] = locations["last_seen_at"]

        with self.connect() as con:
            con.register("incoming_locations", locations)
            con.execute(
                """
                DELETE FROM locations
                WHERE location_id IN (SELECT location_id FROM incoming_locations)
                """
            )
            con.execute(
                """
                INSERT INTO locations
                SELECT location_id, city, country, latitude, longitude, first_seen_at, last_seen_at
                FROM incoming_locations
                """
            )

            con.register("incoming_observations", frame[self._observation_columns()])
            con.execute(
                """
                DELETE FROM weather_observations
                WHERE observation_id IN (SELECT observation_id FROM incoming_observations)
                """
            )
            con.execute(
                """
                INSERT INTO weather_observations
                SELECT * FROM incoming_observations
                """
            )

        return len(frame)

    def query_history(self, city: str, limit: int = 500) -> pd.DataFrame:
        """Return recent persisted observations for one city."""

        with self.connect() as con:
            return con.execute(
                """
                SELECT
                    o.*,
                    l.city,
                    l.country,
                    l.latitude,
                    l.longitude
                FROM weather_observations o
                JOIN locations l ON o.location_id = l.location_id
                WHERE lower(l.city) = lower(?)
                ORDER BY o.observed_at DESC
                LIMIT ?
                """,
                [city, limit],
            ).fetchdf()

    def query_latest_cities(self, limit: int = 25) -> pd.DataFrame:
        """Return latest observed city rows for a compact operations table."""

        with self.connect() as con:
            return con.execute(
                """
                WITH ranked AS (
                    SELECT
                        l.city,
                        l.country,
                        l.latitude,
                        l.longitude,
                        o.observed_at,
                        o.temp_c,
                        o.humidity_pct,
                        o.pressure_hpa,
                        o.wind_speed_kph,
                        o.description,
                        row_number() OVER (
                            PARTITION BY l.location_id
                            ORDER BY o.observed_at DESC
                        ) AS rn
                    FROM locations l
                    JOIN weather_observations o ON l.location_id = o.location_id
                    WHERE o.source = 'current'
                )
                SELECT * EXCLUDE (rn)
                FROM ranked
                WHERE rn = 1
                ORDER BY observed_at DESC
                LIMIT ?
                """,
                [limit],
            ).fetchdf()

    def _request(self, endpoint: str, params: dict[str, Any]) -> dict[str, Any]:
        request_params = {
            **params,
            "appid": self.settings.api_key,
            "units": "metric",
        }
        try:
            response = requests.get(
                f"{BASE_URL}/{endpoint}",
                params=request_params,
                timeout=self.settings.request_timeout_seconds,
            )
            response.raise_for_status()
        except requests.HTTPError as exc:
            detail = response.text[:300] if "response" in locals() else str(exc)
            raise WeatherAcquisitionError(f"OpenWeatherMap request failed: {detail}") from exc
        except requests.RequestException as exc:
            raise WeatherAcquisitionError(f"Weather API request failed: {exc}") from exc

        return response.json()

    def _parse_current(self, payload: dict[str, Any], acquired_at: datetime) -> dict[str, Any]:
        main = payload.get("main", {})
        wind = payload.get("wind", {})
        weather = (payload.get("weather") or [{}])[0]
        coord = payload.get("coord", {})
        observed_at = datetime.fromtimestamp(payload.get("dt", acquired_at.timestamp()), timezone.utc)

        return self._base_row(
            payload=payload,
            source="current",
            city=payload.get("name", "Unknown"),
            country=payload.get("sys", {}).get("country", ""),
            latitude=coord.get("lat"),
            longitude=coord.get("lon"),
            observed_at=observed_at,
            acquired_at=acquired_at,
            main=main,
            wind=wind,
            weather=weather,
            cloud_cover_pct=payload.get("clouds", {}).get("all"),
            visibility_km=self._safe_div(payload.get("visibility"), 1000),
            precipitation_mm=payload.get("rain", {}).get("1h", 0) + payload.get("snow", {}).get("1h", 0),
            precipitation_probability_pct=None,
        )

    def _parse_forecast(self, payload: dict[str, Any], acquired_at: datetime) -> list[dict[str, Any]]:
        city_payload = payload.get("city", {})
        coord = city_payload.get("coord", {})
        rows = []

        for item in payload.get("list", []):
            main = item.get("main", {})
            wind = item.get("wind", {})
            weather = (item.get("weather") or [{}])[0]
            observed_at = datetime.fromtimestamp(item.get("dt", acquired_at.timestamp()), timezone.utc)
            rows.append(
                self._base_row(
                    payload=item,
                    source="forecast_3h",
                    city=city_payload.get("name", "Unknown"),
                    country=city_payload.get("country", ""),
                    latitude=coord.get("lat"),
                    longitude=coord.get("lon"),
                    observed_at=observed_at,
                    acquired_at=acquired_at,
                    main=main,
                    wind=wind,
                    weather=weather,
                    cloud_cover_pct=item.get("clouds", {}).get("all"),
                    visibility_km=self._safe_div(item.get("visibility"), 1000),
                    precipitation_mm=item.get("rain", {}).get("3h", 0) + item.get("snow", {}).get("3h", 0),
                    precipitation_probability_pct=self._safe_mul(item.get("pop"), 100),
                )
            )

        return rows

    def _base_row(
        self,
        payload: dict[str, Any],
        source: str,
        city: str,
        country: str,
        latitude: float | None,
        longitude: float | None,
        observed_at: datetime,
        acquired_at: datetime,
        main: dict[str, Any],
        wind: dict[str, Any],
        weather: dict[str, Any],
        cloud_cover_pct: float | None,
        visibility_km: float | None,
        precipitation_mm: float | None,
        precipitation_probability_pct: float | None,
    ) -> dict[str, Any]:
        return {
            "city": city,
            "country": country,
            "latitude": latitude,
            "longitude": longitude,
            "observed_at": pd.Timestamp(observed_at).tz_convert(None),
            "acquired_at": pd.Timestamp(acquired_at).tz_convert(None),
            "source": source,
            "temp_c": main.get("temp"),
            "feels_like_c": main.get("feels_like"),
            "humidity_pct": main.get("humidity"),
            "pressure_hpa": main.get("pressure"),
            "wind_speed_kph": self._safe_mul(wind.get("speed"), 3.6),
            "wind_direction_deg": wind.get("deg"),
            "cloud_cover_pct": cloud_cover_pct,
            "visibility_km": visibility_km,
            "precipitation_mm": precipitation_mm,
            "precipitation_probability_pct": precipitation_probability_pct,
            "condition_id": weather.get("id"),
            "description": weather.get("description", ""),
            "payload_json": json.dumps(payload, separators=(",", ":"), default=str),
        }

    @staticmethod
    def _safe_mul(value: Any, multiplier: float) -> float | None:
        return None if value is None else float(value) * multiplier

    @staticmethod
    def _safe_div(value: Any, divisor: float) -> float | None:
        return None if value is None else float(value) / divisor

    @staticmethod
    def _stable_hash(value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()[:24]

    def _location_id_from_row(self, row: pd.Series) -> str:
        key = f"{row['city']}|{row['country']}|{row['latitude']:.4f}|{row['longitude']:.4f}".lower()
        return self._stable_hash(key)

    def _observation_id_from_row(self, row: pd.Series) -> str:
        key = f"{row['location_id']}|{row['source']}|{pd.Timestamp(row['observed_at']).isoformat()}"
        return self._stable_hash(key)

    @staticmethod
    def _observation_columns() -> list[str]:
        return [
            "observation_id",
            "location_id",
            "observed_at",
            "acquired_at",
            "source",
            "temp_c",
            "feels_like_c",
            "humidity_pct",
            "pressure_hpa",
            "wind_speed_kph",
            "wind_direction_deg",
            "cloud_cover_pct",
            "visibility_km",
            "precipitation_mm",
            "precipitation_probability_pct",
            "condition_id",
            "description",
            "payload_json",
        ]
