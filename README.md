# Weather Analytics Operations Suite

An advanced weather analytics project upgraded from a student-level terminal
forecast app into a service-oriented analytics suite. The application now
combines live OpenWeatherMap acquisition, DuckDB time-series persistence,
statistical anomaly detection, lightweight predictive modeling, Plotly Graph
Objects, and a Pydeck 3D geospatial layer.

## What Changed

- Added a production-style `src/weather_suite/` package with separate
  configuration, engine, analytics, and visualization layers.
- Replaced CSV-style storage with a DuckDB analytical warehouse stored at
  `data/weather_warehouse.duckdb`.
- Added persistent historical weather storage with deterministic observation ids
  and indexed time-series queries.
- Added anomaly detection for rolling Z-score outliers, sudden pressure drops,
  and temperature jumps.
- Added a lightweight 6-hour regression forecast using scikit-learn.
- Replaced Matplotlib-only charts with custom layered Plotly Graph Objects.
- Added a Pydeck 3D geospatial atmospheric map using weather-driven column
  height, radius, and color.
- Added a Streamlit industrial operations UI in `app.py`.
- Updated `.env.example` to use placeholders only. Real API keys should stay in
  `.env`.
- Updated `.gitignore` so local DuckDB and log files are not committed.

## Directory Structure

```text
Weather-Forecast-Alert-Application/
|-- app.py                         # Streamlit view/controller entrypoint
|-- main.py                        # Legacy terminal application kept for reference
|-- requirements.txt               # Production analytics dependency set
|-- README.md
|-- .env.example                   # Safe placeholder env template
|-- data/
|   |-- weather_warehouse.duckdb    # Runtime DuckDB database, ignored by git
|   |-- simulation.py               # Existing simulation helper
|   |-- sample_current_weather.json
|   |-- sample_forecast.json
|-- src/
|   |-- weather_suite/
|   |   |-- __init__.py
|   |   |-- config.py               # Environment variables and runtime settings
|   |   |-- engine.py               # Acquisition, normalization, DuckDB persistence
|   |   |-- analytics.py            # Outliers and 6-hour regression forecast
|   |   |-- visualizations.py       # Plotly Graph Objects and Pydeck layers
|   |-- api_handler.py              # Legacy helper
|   |-- data_parser.py              # Legacy helper
|   |-- alert_system.py             # Legacy helper
|   |-- visualizer.py               # Legacy helper
```

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set your real OpenWeatherMap key:

```env
WEATHER_API_KEY='your_openweathermap_api_key_here'
WEATHER_DB_PATH='data/weather_warehouse.duckdb'
DEFAULT_CITY='Mumbai'
ANOMALY_Z_THRESHOLD='2.2'
ANOMALY_ROLLING_WINDOW='8'
```

## Run

```powershell
streamlit run app.py
```

If using the local virtual environment directly:

```powershell
.\.venv\Scripts\streamlit.exe run app.py
```

The app opens a dense operations dashboard where you can fetch live data by
city, persist it to DuckDB, inspect anomalies, view the 6-hour forecast, and
explore the 3D atmospheric layer.

## Architecture

The project now follows a service-oriented MVC-style split:

- Model/service: `WeatherEngine` in `src/weather_suite/engine.py`
  fetches OpenWeatherMap current and 3-hour forecast data, normalizes records,
  creates the DuckDB schema, persists observations, and exposes analytical read
  queries.
- Logic/analytics: `WeatherAnalytics` in `src/weather_suite/analytics.py`
  detects statistical outliers and trains a short-horizon regression forecast.
- View/controller: `app.py` manages Streamlit session state, calls the engine
  and analytics layers, and renders charts, tables, metrics, and maps.
- Visualization layer: `src/weather_suite/visualizations.py` builds Plotly
  Graph Objects and Pydeck views without owning acquisition or business logic.

## DuckDB Schema

`locations`

```text
location_id, city, country, latitude, longitude, first_seen_at, last_seen_at
```

`weather_observations`

```text
observation_id, location_id, observed_at, acquired_at, source,
temp_c, feels_like_c, humidity_pct, pressure_hpa, wind_speed_kph,
wind_direction_deg, cloud_cover_pct, visibility_km, precipitation_mm,
precipitation_probability_pct, condition_id, description, payload_json
```

Indexes:

```text
idx_weather_location_time(location_id, observed_at)
idx_weather_source_time(source, observed_at)
```

## Analytics

Anomaly detection includes:

- Rolling Z-score checks across temperature, pressure, humidity, wind, and
  precipitation.
- Sudden pressure-drop detection for storm-risk signals.
- Temperature jump detection for short-horizon weather outliers.

Predictive modeling includes:

- A 6-hour forecast generated from the current cached session.
- Time-based features including elapsed hours and day-cycle sine/cosine terms.
- `HuberRegressor` with scaling when enough rows exist, falling back to linear
  regression or persistence for small samples.

## Visualization

- Main chart: layered Plotly Graph Objects time-series view for temperature,
  feels-like temperature, humidity, pressure, anomalies, and predicted values.
- Secondary chart: pressure-wind coupling scatter/line chart with temperature
  color encoding.
- Geospatial chart: Pydeck 3D `ColumnLayer` where atmospheric values influence
  column height, radius, and color.

## Requirements

Core packages:

```text
duckdb
pandas
numpy
requests
python-dotenv
scikit-learn
streamlit
plotly
pydeck
```

Pinned versions are listed in `requirements.txt`.

## Verification Performed

- Compiled the new Python modules with `py_compile`.
- Installed and aligned the virtual environment with `requirements.txt`.
- Ran `pip check` successfully.
- Ran a smoke test that created a temporary DuckDB database, persisted sample
  observations, queried history, detected anomalies, and generated 6 forecast
  rows.
- Started Streamlit successfully and confirmed the local app responded with HTTP
  `200`.

## Notes

The older terminal app and helper modules are still present for comparison, but
the advanced suite entrypoint is `app.py`. Runtime database files are intentionally
ignored by git so the schema is reproducible while local weather history remains
local.
