"""Plotly and Pydeck rendering helpers."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pydeck as pdk
from plotly.subplots import make_subplots


def build_timeseries_figure(
    observations: pd.DataFrame,
    anomalies: pd.DataFrame,
    predictions: pd.DataFrame,
) -> go.Figure:
    """Build a layered Plotly Graph Objects time-series figure."""

    frame = _prepare(observations)
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    if not frame.empty:
        fig.add_trace(
            go.Scatter(
                x=frame["observed_at"],
                y=frame["temp_c"],
                mode="lines+markers",
                name="Temperature C",
                line={"color": "#f97316", "width": 2},
                marker={"size": 6},
                hovertemplate="%{x}<br>%{y:.1f} C<extra>Temperature</extra>",
            ),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(
                x=frame["observed_at"],
                y=frame["feels_like_c"],
                mode="lines",
                name="Feels Like C",
                line={"color": "#facc15", "width": 1.5, "dash": "dot"},
                hovertemplate="%{x}<br>%{y:.1f} C<extra>Feels Like</extra>",
            ),
            secondary_y=False,
        )
        fig.add_trace(
            go.Bar(
                x=frame["observed_at"],
                y=frame["humidity_pct"],
                name="Humidity %",
                marker={"color": "rgba(14, 165, 233, 0.28)"},
                hovertemplate="%{x}<br>%{y:.0f}%<extra>Humidity</extra>",
            ),
            secondary_y=True,
        )
        fig.add_trace(
            go.Scatter(
                x=frame["observed_at"],
                y=frame["pressure_hpa"],
                mode="lines",
                name="Pressure hPa",
                line={"color": "#22c55e", "width": 1.8},
                hovertemplate="%{x}<br>%{y:.0f} hPa<extra>Pressure</extra>",
            ),
            secondary_y=True,
        )

    if predictions is not None and not predictions.empty and "temp_c" in predictions:
        fig.add_trace(
            go.Scatter(
                x=predictions["forecast_at"],
                y=predictions["temp_c"],
                mode="lines+markers",
                name="6h ML Forecast",
                line={"color": "#e11d48", "width": 2.5, "dash": "dash"},
                marker={"symbol": "diamond", "size": 7},
                hovertemplate="%{x}<br>%{y:.1f} C<extra>Predicted</extra>",
            ),
            secondary_y=False,
        )

    if anomalies is not None and not anomalies.empty and not frame.empty:
        temp_anomalies = anomalies[anomalies["metric"].eq("temp_c")]
        if not temp_anomalies.empty:
            fig.add_trace(
                go.Scatter(
                    x=temp_anomalies["observed_at"],
                    y=temp_anomalies["value"],
                    mode="markers",
                    name="Temperature Outliers",
                    marker={
                        "size": 13,
                        "color": "#dc2626",
                        "symbol": "x",
                        "line": {"width": 2, "color": "#fee2e2"},
                    },
                    hovertemplate="%{x}<br>%{text}<extra>Outlier</extra>",
                    text=temp_anomalies["reason"],
                ),
                secondary_y=False,
            )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b1120",
        plot_bgcolor="#101827",
        margin={"l": 24, "r": 24, "t": 36, "b": 24},
        height=430,
        legend={"orientation": "h", "y": 1.12, "x": 0},
        hovermode="x unified",
        title={"text": "Atmospheric Signal Stack", "font": {"size": 16}},
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(148,163,184,0.12)")
    fig.update_yaxes(title_text="Temperature C", secondary_y=False, gridcolor="rgba(148,163,184,0.12)")
    fig.update_yaxes(title_text="Humidity / Pressure", secondary_y=True, showgrid=False)
    return fig


def build_wind_pressure_figure(observations: pd.DataFrame) -> go.Figure:
    """Build a second operational chart for pressure and wind coupling."""

    frame = _prepare(observations)
    fig = go.Figure()
    if not frame.empty:
        fig.add_trace(
            go.Scatter(
                x=frame["pressure_hpa"],
                y=frame["wind_speed_kph"],
                mode="markers+lines",
                name="Pressure vs Wind",
                marker={
                    "size": np.clip(frame["humidity_pct"].fillna(40) / 5, 7, 18),
                    "color": frame["temp_c"],
                    "colorscale": "Turbo",
                    "showscale": True,
                    "colorbar": {"title": "C"},
                },
                line={"color": "rgba(148,163,184,0.45)", "width": 1},
                text=frame["observed_at"].dt.strftime("%Y-%m-%d %H:%M"),
                hovertemplate="Pressure %{x:.0f} hPa<br>Wind %{y:.1f} kph<br>%{text}<extra></extra>",
            )
        )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b1120",
        plot_bgcolor="#101827",
        margin={"l": 24, "r": 24, "t": 36, "b": 24},
        height=330,
        title={"text": "Pressure-Wind Coupling", "font": {"size": 16}},
        xaxis_title="Pressure hPa",
        yaxis_title="Wind speed kph",
    )
    return fig


def build_atmospheric_deck(observations: pd.DataFrame) -> pdk.Deck | None:
    """Create a 3D geospatial atmospheric layer using Pydeck."""

    frame = _prepare(observations)
    if frame.empty or frame[["latitude", "longitude"]].dropna().empty:
        return None

    geo = frame.dropna(subset=["latitude", "longitude"]).copy()
    geo["lead_hours"] = (geo["observed_at"] - geo["observed_at"].min()).dt.total_seconds() / 3600.0
    geo["bearing"] = np.deg2rad(geo["wind_direction_deg"].fillna(0))
    geo["map_latitude"] = geo["latitude"] + np.cos(geo["bearing"]) * geo["lead_hours"] * 0.012
    geo["map_longitude"] = geo["longitude"] + np.sin(geo["bearing"]) * geo["lead_hours"] * 0.012
    geo["elevation"] = (geo["pressure_hpa"].fillna(1000) - 930).clip(lower=5) * 45
    geo["radius"] = np.clip(geo["wind_speed_kph"].fillna(8) * 70, 450, 2800)
    geo["color"] = geo["temp_c"].apply(_temperature_color)

    center_lat = float(geo["latitude"].iloc[0])
    center_lon = float(geo["longitude"].iloc[0])

    layer = pdk.Layer(
        "ColumnLayer",
        data=geo,
        get_position=["map_longitude", "map_latitude"],
        get_elevation="elevation",
        elevation_scale=1,
        radius="radius",
        get_fill_color="color",
        pickable=True,
        auto_highlight=True,
    )

    return pdk.Deck(
        map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
        initial_view_state=pdk.ViewState(
            latitude=center_lat,
            longitude=center_lon,
            zoom=8,
            pitch=48,
            bearing=22,
        ),
        layers=[layer],
        tooltip={
            "html": "<b>{observed_at}</b><br/>Temp: {temp_c} C<br/>Pressure: {pressure_hpa} hPa<br/>Wind: {wind_speed_kph} kph",
            "style": {"backgroundColor": "#0f172a", "color": "#f8fafc"},
        },
    )


def _prepare(observations: pd.DataFrame) -> pd.DataFrame:
    if observations is None or observations.empty:
        return pd.DataFrame()

    frame = observations.copy()
    frame["observed_at"] = pd.to_datetime(frame["observed_at"], errors="coerce")
    frame = frame.dropna(subset=["observed_at"]).sort_values("observed_at")
    for column in [
        "temp_c",
        "feels_like_c",
        "humidity_pct",
        "pressure_hpa",
        "wind_speed_kph",
        "wind_direction_deg",
        "latitude",
        "longitude",
    ]:
        if column in frame.columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
    return frame


def _temperature_color(temp_c: float | None) -> list[int]:
    if pd.isna(temp_c):
        return [148, 163, 184, 170]
    if temp_c >= 35:
        return [220, 38, 38, 190]
    if temp_c >= 28:
        return [249, 115, 22, 185]
    if temp_c >= 20:
        return [34, 197, 94, 180]
    return [14, 165, 233, 180]
