<div align="center">

<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/DuckDB-FFF000?style=for-the-badge&logo=duckdb&logoColor=black"/>
<img src="https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"/>
<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
<img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white"/>
<img src="https://img.shields.io/badge/Pydeck-00A8E8?style=for-the-badge&logo=mapbox&logoColor=white"/>

<br/><br/>

# 🌦️ Weather Analytics Operations Suite

### Enterprise-style weather intelligence platform with DuckDB, anomaly detection, forecasting, and 3D atmospheric visualization

[![License](https://img.shields.io/badge/License-CC%20BY--NC%204.0-green.svg)](LICENSE)
[![Database](https://img.shields.io/badge/Database-DuckDB-yellow)](https://duckdb.org/)
[![Models](https://img.shields.io/badge/Models-HuberRegressor%20%2B%20Z--Score-orange)]()
[![Visualization](https://img.shields.io/badge/Viz-Plotly%20%2B%20Pydeck-blue)]()
[![UI](https://img.shields.io/badge/UI-Streamlit-red)]()
[![Status](https://img.shields.io/badge/Status-Active-success)]()

<br/>

</div>

---

## 📌 Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Industry Relevance](#industry-relevance)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Database Schema](#database-schema)
- [Analytics Engine](#analytics-engine)
- [Visualization Layer](#visualization-layer)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Verification Performed](#verification-performed)
- [Learning Outcomes](#learning-outcomes)
- [Future Improvements](#future-improvements)
- [License](#license)

---

<a id="overview"></a>

## 🔍 Overview

The **Weather Analytics Operations Suite** is an advanced service-oriented weather intelligence platform designed to transform raw meteorological data into actionable operational insights.

Originally upgraded from a student-level terminal forecasting application, the system now mirrors the architecture and workflow of industrial monitoring platforms used in logistics, aviation, agriculture, marine operations, and environmental analytics.

The platform combines:

- **Live OpenWeatherMap API acquisition**
- **DuckDB analytical time-series warehousing**
- **Statistical anomaly detection**
- **Short-horizon predictive forecasting**
- **Plotly Graph Objects visualization**
- **Pydeck-powered 3D atmospheric mapping**
- **Streamlit operational dashboard UI**

The application stores persistent historical weather records, performs analytical queries in milliseconds, detects abnormal atmospheric patterns, and visualizes spatial weather conditions using layered industrial-grade dashboards.

---

<a id="problem-statement"></a>

## ❗ Problem Statement

Traditional weather applications focus only on displaying current conditions and short forecasts. They generally lack the analytical depth required for operational or industrial decision-making.

Common limitations include:

- **No Historical Persistence**  
  Most apps discard weather history after display, preventing long-term comparisons and analytics.

- **No Statistical Intelligence**  
  Temperature, pressure, and humidity changes are shown without identifying outliers or anomaly risks.

- **Lack of Predictive Insight**  
  Users must manually interpret whether environmental changes indicate incoming storms or instability.

- **Limited Visualization**  
  Standard 2D interfaces fail to represent atmospheric density, pressure layers, or spatial relationships.

- **No Operational Dashboarding**  
  Consumer-focused UIs are not designed for analytical monitoring or multi-city operational workflows.

This project addresses those gaps by combining persistence, analytics, predictive modeling, and advanced visualization into a single platform.

---

<a id="industry-relevance"></a>

## 🏭 Industry Relevance

| Industry | Real-World Use Case | Equivalent Systems |
|---|---|---|
| **Agriculture** | Monitor rainfall, humidity, and pressure anomalies for crop planning | Precision farming analytics platforms |
| **Aviation** | Detect sudden pressure changes and storm-risk indicators | Aviation weather intelligence systems |
| **Logistics & Shipping** | Track environmental conditions across operational regions | Fleet weather monitoring platforms |
| **Energy & Utilities** | Forecast weather-driven operational disruptions | Utility forecasting dashboards |
| **Smart Cities** | Monitor atmospheric conditions and urban climate patterns | Urban environmental monitoring systems |
| **Disaster Management** | Identify rapid atmospheric instability before severe weather events | Early warning analytics systems |
| **Research & Academia** | Time-series atmospheric analysis and anomaly modeling | Environmental data science platforms |

The workflow mirrors modern operational pipelines:

```text
API Acquisition → Time-Series Storage → Analytics → Forecasting → Dashboard Visualization
```

---

<a id="system-architecture"></a>

## 🏗️ System Architecture

```text
+-----------------------------------------------------------+
|                      INPUT LAYER                          |
|          OpenWeatherMap API (Current & Forecast)          |
+---------------------------+-------------------------------+
                            |
                            v
+-----------------------------------------------------------+
|                   SERVICE-ORIENTED ENGINE                 |
| * Data Normalization      * Deterministic ID Generation   |
| * DuckDB Persistence      * Multi-city Handling           |
+---------------------------+-------------------------------+
                            |
                            v
+-----------------------------------------------------------+
|                   ANALYTICS ENGINE                        |
|                                                           |
| [ ANOMALY DETECTION ]        [ PREDICTIVE MODEL ]         |
|  - Rolling Z-Scores           - HuberRegressor            |
|  - Pressure Drop logic        - 6-hour forecast           |
+---------------------------+-------------------------------+
                            |
                            v
+-----------------------------------------------------------+
|                    OUTPUT LAYER                           |
| * Streamlit UI            * 3D Atmospheric Map            |
| * Anomaly Risk Logs       * weather_warehouse.duckdb      |
+-----------------------------------------------------------+
```

---

<a id="tech-stack"></a>

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|---|---|---|
| Database | DuckDB | High-performance OLAP time-series storage |
| Backend Engine | Python 3.10+ | Core implementation and orchestration |
| Modeling | Scikit-learn | Regression forecasting and anomaly analytics |
| Frontend | Streamlit | Industrial operations dashboard |
| Visualization (2D) | Plotly Graph Objects | Interactive multi-layered time-series charts |
| Visualization (3D) | Pydeck | Atmospheric geospatial visualization |
| Data Processing | Pandas & NumPy | Transformation and analytical processing |
| API Integration | Requests | OpenWeatherMap acquisition |

---

<a id="database-schema"></a>

## 🗄️ Database Schema

### `locations`

```text
location_id, city, country, latitude, longitude, first_seen_at, last_seen_at
```

### `weather_observations`

```text
observation_id, location_id, observed_at, acquired_at, source,
temp_c, feels_like_c, humidity_pct, pressure_hpa, wind_speed_kph,
wind_direction_deg, cloud_cover_pct, visibility_km, precipitation_mm,
precipitation_probability_pct, condition_id, description, payload_json
```

### Indexed Queries

```text
idx_weather_location_time(location_id, observed_at)
idx_weather_source_time(source, observed_at)
```

---

<a id="analytics-engine"></a>

## 🤖 Analytics Engine

### Anomaly Detection

- Rolling Z-score anomaly detection
- Sudden atmospheric pressure-drop analysis
- Temperature jump detection
- Humidity instability analysis
- Wind fluctuation monitoring

### Predictive Forecasting

- 6-hour short-horizon forecasting
- Time-based cyclical feature engineering
- Day-cycle sine/cosine transformations
- `HuberRegressor` robust regression modeling
- Automatic fallback logic for small datasets

---

<a id="visualization-layer"></a>

## 📊 Visualization Layer

### Main Dashboard

- Multi-layer Plotly Graph Objects time-series visualization
- Temperature vs. feels-like comparisons
- Pressure and humidity overlays
- Forecast prediction visualization
- Statistical anomaly markers

### 3D Atmospheric Mapping

- Atmospheric density visualization
- Spatial pressure intensity mapping
- Weather-driven column height rendering
- Color-scaled environmental conditions

---

<a id="project-structure"></a>

## 📁 Project Structure

```text
Weather-Forecast-Alert-Application/
|
|-- app.py                         <-- Streamlit operations dashboard
|-- main.py                        <-- Legacy terminal application
|-- requirements.txt               <-- Dependency set
|-- README.md
|-- LICENSE
|-- .env.example                   <-- Environment template
|
|-- data/
|   |-- weather_warehouse.duckdb   <-- Runtime DuckDB database
|   |-- simulation.py
|   |-- sample_current_weather.json
|   |-- sample_forecast.json
|
|-- src/
|   |-- weather_suite/
|   |   |-- __init__.py
|   |   |-- config.py
|   |   |-- engine.py
|   |   |-- analytics.py
|   |   |-- visualizations.py
|   |
|   |-- api_handler.py
|   |-- data_parser.py
|   |-- alert_system.py
|   |-- visualizer.py
```

---

<a id="installation"></a>

## ⚙️ Installation

### Step 1 — Clone Repository

```powershell
git clone https://github.com/CH-S-K-CHAITANYA/Weather-Forecast-Alert-Application.git
cd Weather-Forecast-Alert-Application
```

### Step 2 — Create Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### Step 3 — Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 4 — Configure Environment Variables

Copy `.env.example` to `.env` and configure your OpenWeatherMap API key.

```env
WEATHER_API_KEY='your_openweathermap_api_key_here'
WEATHER_DB_PATH='data/weather_warehouse.duckdb'
DEFAULT_CITY='Mumbai'
ANOMALY_Z_THRESHOLD='2.2'
ANOMALY_ROLLING_WINDOW='8'
```

---

<a id="how-to-run"></a>

## ▶️ How to Run

### Launch Streamlit Dashboard

```powershell
streamlit run app.py
```

### Run Using Local Virtual Environment

```powershell
.\.venv\Scripts\streamlit.exe run app.py
```

The application launches a full operational analytics dashboard where users can:

- Fetch live weather data
- Persist observations into DuckDB
- Detect anomalies
- Generate short-horizon forecasts
- Explore 3D atmospheric layers
- Visualize operational weather metrics

---

<a id="verification-performed"></a>

## ✅ Verification Performed

- Python modules compiled using `py_compile`
- Dependencies aligned with `requirements.txt`
- `pip check` executed successfully
- DuckDB persistence smoke tests passed
- Historical weather queries validated
- Forecast generation verified
- Streamlit application launched successfully
- Local HTTP response confirmed with status `200`

---

<a id="learning-outcomes"></a>

## 🎓 Learning Outcomes

### Data Engineering

- DuckDB analytical warehousing
- Persistent time-series storage
- Structured environmental data modeling
- Indexed analytical querying

### Machine Learning & Analytics

- Robust regression forecasting
- Statistical anomaly detection
- Time-based feature engineering
- Atmospheric pattern analysis

### Visualization Engineering

- Plotly Graph Objects dashboarding
- 3D Pydeck geospatial rendering
- Multi-layer operational visualization

### Software Architecture

- Service-oriented application structure
- MVC-inspired separation of concerns
- Streamlit operational UI development
- Environment-driven configuration management

---

<a id="future-improvements"></a>

## 🔮 Future Improvements

- [ ] Real-time weather streaming pipeline
- [ ] Kafka-based ingestion architecture
- [ ] Multi-region atmospheric clustering
- [ ] LSTM forecasting for temporal weather modeling
- [ ] Severe weather alert notifications
- [ ] Docker containerization
- [ ] FastAPI REST endpoints
- [ ] Historical climate trend analytics
- [ ] Satellite imagery overlay integration
- [ ] Kubernetes deployment support

---

<a id="license"></a>


## 📄 License

This project is licensed under the
[Creative Commons Attribution-NonCommercial 4.0 International License](LICENSE).

Commercial usage, monetization, SaaS deployment,
or proprietary redistribution is prohibited
without explicit written permission from the author.

Full License:
https://creativecommons.org/licenses/by-nc/4.0/

---

<div align="center">

## 👨‍💻 Author

### **CH S K CHAITANYA**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/chskchaitanya)

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/CH-S-K-CHAITANYA)


⭐ If you found this project useful, consider starring the repository.



</div>
