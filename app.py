"""Streamlit UI for the production-grade weather analytics suite."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.weather_suite import WeatherAnalytics, WeatherEngine, load_settings
from src.weather_suite.engine import WeatherAcquisitionError
from src.weather_suite.visualizations import (
    build_atmospheric_deck,
    build_timeseries_figure,
    build_wind_pressure_figure,
)


st.set_page_config(
    page_title="Weather Analytics Operations Suite",
    page_icon="WA",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background: #080c14;
            color: #e5e7eb;
        }
        [data-testid="stSidebar"] {
            background: #0b1120;
            border-right: 1px solid rgba(148, 163, 184, 0.18);
        }
        .metric-strip {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 0.65rem;
            margin: 0.3rem 0 1rem;
        }
        .metric-cell {
            border: 1px solid rgba(148, 163, 184, 0.2);
            background: #101827;
            padding: 0.8rem 0.9rem;
            border-radius: 6px;
        }
        .metric-label {
            color: #94a3b8;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0;
        }
        .metric-value {
            color: #f8fafc;
            font-size: 1.35rem;
            line-height: 1.5rem;
            font-weight: 700;
        }
        .section-title {
            color: #e2e8f0;
            font-size: 0.95rem;
            font-weight: 700;
            margin: 0.4rem 0 0.6rem;
            text-transform: uppercase;
            letter-spacing: 0;
        }
        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(148, 163, 184, 0.16);
        }
        @media (max-width: 900px) {
            .metric-strip { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_resource
def get_engine() -> WeatherEngine:
    return WeatherEngine(load_settings())


def metric_strip(summary: dict[str, float | int], city: str) -> None:
    def fmt(value: float | int, suffix: str = "") -> str:
        if pd.isna(value):
            return "NA"
        if isinstance(value, float):
            return f"{value:.1f}{suffix}"
        return f"{value}{suffix}"

    st.markdown(
        f"""
        <div class="metric-strip">
            <div class="metric-cell"><div class="metric-label">Station</div><div class="metric-value">{city}</div></div>
            <div class="metric-cell"><div class="metric-label">Latest Temp</div><div class="metric-value">{fmt(summary["temp_latest"], " C")}</div></div>
            <div class="metric-cell"><div class="metric-label">Pressure</div><div class="metric-value">{fmt(summary["pressure_latest"], " hPa")}</div></div>
            <div class="metric-cell"><div class="metric-label">Wind</div><div class="metric-value">{fmt(summary["wind_latest"], " kph")}</div></div>
            <div class="metric-cell"><div class="metric-label">Outliers</div><div class="metric-value">{summary["anomalies"]}</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def load_history_or_session(engine: WeatherEngine, city: str) -> pd.DataFrame:
    history = engine.query_history(city, limit=600)
    session_frame = st.session_state.get("session_observations")
    if session_frame is not None and not session_frame.empty:
        return pd.concat([history, session_frame], ignore_index=True).drop_duplicates(
            ["observed_at", "source"],
            keep="last",
        )
    return history


def main() -> None:
    inject_styles()
    settings = load_settings()
    engine = get_engine()
    analytics = WeatherAnalytics()

    st.sidebar.header("Acquisition")
    city = st.sidebar.text_input("City", value=st.session_state.get("city", settings.default_city))
    z_threshold = st.sidebar.slider("Z-score threshold", 1.5, 4.0, settings.anomaly_z_threshold, 0.1)
    rolling_window = st.sidebar.slider("Rolling window", 4, 24, settings.rolling_window, 1)
    fetch_clicked = st.sidebar.button("Fetch live data", type="primary", use_container_width=True)

    if fetch_clicked:
        try:
            snapshot = engine.fetch_city_snapshot(city)
            st.session_state["city"] = snapshot.city
            st.session_state["session_observations"] = snapshot.combined
            st.sidebar.success(f"Persisted {len(snapshot.combined)} rows to DuckDB")
        except WeatherAcquisitionError as exc:
            st.sidebar.error(str(exc))

    selected_city = st.session_state.get("city", city)
    observations = load_history_or_session(engine, selected_city)
    anomalies = analytics.detect_anomalies(
        observations,
        rolling_window=rolling_window,
        z_threshold=z_threshold,
    )
    predictions = analytics.forecast_next_6_hours(st.session_state.get("session_observations", observations))
    summary = analytics.summarize_operations(observations, anomalies)

    st.title("Weather Analytics Operations Suite")
    metric_strip(summary, selected_city)

    left, right = st.columns([1.35, 1], gap="medium")
    with left:
        st.markdown('<div class="section-title">Signal Intelligence</div>', unsafe_allow_html=True)
        st.plotly_chart(
            build_timeseries_figure(observations, anomalies, predictions),
            use_container_width=True,
            config={"displayModeBar": False},
        )
        st.plotly_chart(
            build_wind_pressure_figure(observations),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with right:
        st.markdown('<div class="section-title">3D Atmospheric Field</div>', unsafe_allow_html=True)
        deck = build_atmospheric_deck(observations)
        if deck is None:
            st.info("Fetch live city data to initialize the geospatial layer.")
        else:
            st.pydeck_chart(deck, use_container_width=True)

        st.markdown('<div class="section-title">Anomaly Register</div>', unsafe_allow_html=True)
        if anomalies.empty:
            st.success("No statistical outliers detected for the selected threshold.")
        else:
            st.dataframe(
                anomalies[
                    [
                        "observed_at",
                        "source",
                        "metric",
                        "value",
                        "severity",
                        "reason",
                    ]
                ],
                hide_index=True,
                use_container_width=True,
                height=260,
            )

    lower_left, lower_right = st.columns([1, 1], gap="medium")
    with lower_left:
        st.markdown('<div class="section-title">6 Hour Predictive Model</div>', unsafe_allow_html=True)
        if predictions.empty:
            st.info("Prediction needs at least one cached acquisition.")
        else:
            st.dataframe(
                predictions[
                    [
                        "forecast_at",
                        "temp_c",
                        "pressure_hpa",
                        "humidity_pct",
                        "wind_speed_kph",
                        "confidence",
                    ]
                ],
                hide_index=True,
                use_container_width=True,
                height=255,
            )

    with lower_right:
        st.markdown('<div class="section-title">Warehouse Sample</div>', unsafe_allow_html=True)
        latest_cities = engine.query_latest_cities(limit=25)
        if latest_cities.empty:
            st.info("No persisted city records yet.")
        else:
            st.dataframe(latest_cities, hide_index=True, use_container_width=True, height=255)

    with st.expander("DuckDB schema and data engineering notes", expanded=False):
        st.code(
            f"""
Database: {settings.db_path}

Tables:
  locations(location_id, city, country, latitude, longitude, first_seen_at, last_seen_at)
  weather_observations(observation_id, location_id, observed_at, acquired_at, source,
                       temp_c, feels_like_c, humidity_pct, pressure_hpa, wind_speed_kph,
                       cloud_cover_pct, visibility_km, precipitation_mm, payload_json)

Indexes:
  idx_weather_location_time(location_id, observed_at)
  idx_weather_source_time(source, observed_at)
            """.strip(),
            language="text",
        )


if __name__ == "__main__":
    main()
