<div align="center">

<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/DuckDB-FFF000?style=for-the-badge&logo=duckdb&logoColor=black"/>
<img src="https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"/>
<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
<img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white"/>
<img src="https://img.shields.io/badge/Pydeck-00A8E8?style=for-the-badge&logo=mapbox&logoColor=white"/>
<img src="https://img.shields.io/badge/Time--Series-Analytics-success?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Forecasting-HuberRegressor-orange?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Anomaly-Detection-critical?style=for-the-badge"/>

<br/><br/>

# 🌦️ Weather Analytics Operations Suite

### Enterprise-grade atmospheric intelligence platform featuring DuckDB warehousing, anomaly detection, predictive forecasting, operational analytics, and immersive 3D geospatial visualization

[![License](https://img.shields.io/badge/License-CC%20BY--NC%204.0-green.svg)](LICENSE)
[![Database](https://img.shields.io/badge/Database-DuckDB-yellow)](https://duckdb.org/)
[![Analytics](https://img.shields.io/badge/Analytics-Time%20Series-blue)]()
[![Forecasting](https://img.shields.io/badge/Forecasting-HuberRegressor-orange)]()
[![Visualization](https://img.shields.io/badge/Viz-Plotly%20%2B%20Pydeck-blue)]()
[![Status](https://img.shields.io/badge/Status-Production--Style-success)]()

<br/>

</div>

---

## 📌 Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Core Features](#core-features)
- [Industry Relevance](#industry-relevance)
- [System Architecture](#system-architecture)
- [Operational Workflow](#operational-workflow)
- [Tech Stack](#tech-stack)
- [Database Schema](#database-schema)
- [Analytics Engine](#analytics-engine)
- [Forecasting Pipeline](#forecasting-pipeline)
- [Visualization Layer](#visualization-layer)
- [Dashboard Layer](#dashboard-layer)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Screenshots & Outputs](#screenshots--outputs)
- [Verification Performed](#verification-performed)
- [Security & Reliability](#security--reliability)
- [Learning Outcomes](#learning-outcomes)
- [Future Improvements](#future-improvements)
- [License](#license)

---

<a id="overview"></a>

## 🔍 Overview

The **Weather Analytics Operations Suite** is an enterprise-style weather intelligence platform engineered to transform live atmospheric observations into actionable operational insights through analytics, forecasting, anomaly detection, and geospatial visualization.

Originally evolved from a traditional terminal-based weather forecasting utility, the system now mirrors the architecture and operational workflow of industrial environmental monitoring platforms used across logistics, aviation, utilities, marine operations, agriculture, and disaster management systems.

The platform combines:

- **Live OpenWeatherMap API ingestion**
- **DuckDB analytical time-series warehousing**
- **Operational anomaly detection**
- **Short-horizon predictive forecasting**
- **Plotly Graph Objects dashboard analytics**
- **Pydeck-powered 3D atmospheric rendering**
- **Streamlit operational monitoring UI**
- **Historical environmental persistence**
- **Multi-city atmospheric analytics**

Unlike consumer-grade weather applications that focus purely on presentation, this platform introduces persistent analytical storage, predictive intelligence, atmospheric anomaly monitoring, and recruiter-grade software architecture.

The system demonstrates engineering concepts commonly used in:

- Environmental intelligence platforms
- Aviation weather systems
- Smart city infrastructure
- Climate analytics pipelines
- Operational forecasting systems
- Geospatial monitoring applications
- Data warehousing workflows
- Time-series analytical systems

---

<a id="problem-statement"></a>

## ❗ Problem Statement

Most weather applications focus only on displaying current weather conditions and short-term forecasts. They rarely provide the analytical depth required for operational intelligence or industrial decision-making.

This introduces several limitations:

- **No Historical Persistence**  
  Consumer weather applications discard atmospheric history after display, preventing long-term environmental analysis.

- **No Operational Analytics**  
  Environmental changes are shown without identifying instability, outliers, or weather-risk anomalies.

- **Limited Predictive Intelligence**  
  Users manually interpret trends without analytical forecasting assistance.

- **No Time-Series Warehousing**  
  Weather records are rarely persisted for structured querying or operational reporting.

- **Poor Geospatial Representation**  
  Traditional 2D weather interfaces fail to represent atmospheric density and spatial pressure gradients.

- **No Industrial Monitoring Dashboard**  
  Consumer applications lack operational visibility for multi-location monitoring workflows.

This project addresses those limitations by combining persistent analytical storage, anomaly intelligence, predictive forecasting, and advanced visualization into a unified atmospheric operations platform.

---

<a id="core-features"></a>

## 🚀 Core Features

### Weather Acquisition Engine

- Live OpenWeatherMap API integration
- Multi-city weather ingestion
- Structured JSON normalization
- Persistent environmental warehousing
- Deterministic observation handling

### DuckDB Analytical Warehousing

- Time-series atmospheric persistence
- Indexed environmental queries
- High-performance OLAP-style analytics
- Historical climate comparison workflows
- Lightweight analytical storage engine

### Anomaly Detection System

- Rolling Z-score anomaly detection
- Atmospheric pressure-drop analysis
- Temperature spike identification
- Humidity instability monitoring
- Wind fluctuation intelligence

### Predictive Forecasting

- 6-hour short-horizon forecasting
- HuberRegressor robust regression modeling
- Cyclical feature engineering
- Trend-based weather projection
- Small-dataset fallback protection

### Visualization & Mapping

- Interactive Plotly analytics dashboards
- Time-series atmospheric charts
- Forecast overlays and confidence trends
- 3D atmospheric rendering using Pydeck
- Spatial weather intensity visualization

### Operational Dashboard

- Streamlit monitoring interface
- Multi-city operational analytics
- Atmospheric monitoring workspace
- Recruiter-grade SaaS-inspired UI
- Real-time analytical visualization

---

<a id="industry-relevance"></a>

## 🏭 Industry Relevance

| Industry | Operational Use Case | Equivalent Enterprise Systems |
|---|---|---|
| **Agriculture** | Rainfall and humidity intelligence for crop planning | Precision farming analytics |
| **Aviation** | Atmospheric pressure instability monitoring | Aviation weather intelligence systems |
| **Logistics & Shipping** | Weather-driven operational planning | Fleet environmental monitoring |
| **Energy & Utilities** | Environmental disruption forecasting | Utility forecasting platforms |
| **Smart Cities** | Urban atmospheric monitoring | Climate intelligence systems |
| **Disaster Management** | Early instability detection | Emergency alert analytics |
| **Research & Academia** | Time-series atmospheric analysis | Environmental data science platforms |

The operational workflow mirrors modern weather intelligence systems:

```text
API Acquisition → Time-Series Warehousing → Analytics → Forecasting → Dashboard Visualization
```

---

<a id="system-architecture"></a>

## 🏗️ System Architecture

```text
+----------------------------------------------------------------+
|                         INPUT LAYER                            |
|      OpenWeatherMap API (Current Weather + Forecast Data)      |
+--------------------------------+-------------------------------+
                                 |
                                 v
+----------------------------------------------------------------+
|                  INGESTION & STORAGE ENGINE                    |
| * JSON Normalization       * Deterministic IDs                 |
| * Multi-city Acquisition   * DuckDB Persistence                |
| * Environmental ETL        * Historical Warehousing            |
+--------------------------------+-------------------------------+
                                 |
                                 v
+----------------------------------------------------------------+
|                      ANALYTICS ENGINE                          |
|                                                                |
| [ ANOMALY DETECTION ]         [ FORECASTING PIPELINE ]         |
|                                                                |
| * Rolling Z-Scores            * HuberRegressor                 |
| * Pressure-drop Logic         * Time-based Features            |
| * Humidity Variance           * 6-Hour Prediction Window       |
| * Temperature Instability     * Fallback Forecast Logic        |
+--------------------------------+-------------------------------+
                                 |
                                 v
+----------------------------------------------------------------+
|                       VISUALIZATION LAYER                      |
| * Plotly Operational Charts  * Pydeck 3D Atmospheric Maps      |
| * Forecast Dashboards        * Environmental KPI Panels        |
+--------------------------------+-------------------------------+
                                 |
                                 v
+----------------------------------------------------------------+
|                        DASHBOARD LAYER                         |
| * Streamlit Operations UI    * Multi-city Monitoring           |
| * Anomaly Visibility         * Historical Query Analytics      |
+----------------------------------------------------------------+
```

---

<a id="operational-workflow"></a>

## ⚙️ Operational Workflow

```text
1. Acquire Weather Data from API
               ↓
2. Normalize Atmospheric Payloads
               ↓
3. Persist Records into DuckDB
               ↓
4. Execute Historical Queries
               ↓
5. Run Anomaly Detection Engine
               ↓
6. Generate Forecast Predictions
               ↓
7. Build Time-Series Analytics
               ↓
8. Render 2D & 3D Visualizations
               ↓
9. Display Insights in Dashboard
```

---

<a id="tech-stack"></a>

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|---|---|---|
| Database | DuckDB | High-performance OLAP time-series storage |
| Backend Engine | Python 3.10+ | Core orchestration and weather processing |
| Data Processing | Pandas & NumPy | Analytical transformation workflows |
| Forecasting | Scikit-learn | Regression forecasting models |
| Dashboard UI | Streamlit | Operational monitoring dashboard |
| Visualization (2D) | Plotly Graph Objects | Interactive atmospheric analytics |
| Visualization (3D) | Pydeck | Geospatial atmospheric rendering |
| API Integration | Requests | OpenWeatherMap acquisition |
| Environment Config | python-dotenv | Environment-based configuration |
| Statistical Analytics | SciPy / NumPy | Z-score anomaly calculations |

---

<a id="database-schema"></a>

## 🗄️ Database Schema

### `locations`

```text
location_id, city, country, latitude, longitude,
first_seen_at, last_seen_at
```

### `weather_observations`

```text
observation_id, location_id, observed_at, acquired_at, source,
temp_c, feels_like_c, humidity_pct, pressure_hpa,
wind_speed_kph, wind_direction_deg, cloud_cover_pct,
visibility_km, precipitation_mm,
precipitation_probability_pct,
condition_id, description, payload_json
```

### Indexed Query Strategy

```text
idx_weather_location_time(location_id, observed_at)
idx_weather_source_time(source, observed_at)
```

### Warehousing Design Goals

| Design Goal | Implementation |
|---|---|
| Fast analytical querying | DuckDB OLAP engine |
| Historical persistence | Time-series warehousing |
| Structured weather ETL | Deterministic normalization |
| Operational scalability | Indexed observation retrieval |

---

<a id="analytics-engine"></a>

## 🤖 Analytics Engine

### Atmospheric Anomaly Detection

The analytics engine continuously evaluates weather records to identify statistically abnormal environmental conditions.

Detection logic includes:

- Rolling Z-score deviation analysis
- Sudden pressure-drop identification
- Temperature jump detection
- Wind volatility monitoring
- Humidity instability scoring

### Statistical Processing

```text
Rolling Mean → Standard Deviation →
Z-Score Computation → Threshold Evaluation →
Anomaly Classification
```

### Risk Indicators

| Indicator | Operational Meaning |
|---|---|
| Pressure Drop | Potential storm instability |
| Humidity Spike | Rapid atmospheric saturation |
| Wind Surge | Turbulence or weather-front activity |
| Temperature Jump | Environmental transition anomaly |

---

<a id="forecasting-pipeline"></a>

## 📈 Forecasting Pipeline

### Predictive Modeling

The forecasting subsystem uses `HuberRegressor` to generate short-horizon weather predictions resilient to outliers and noisy atmospheric datasets.

### Forecasting Workflow

```text
Historical Weather →
Feature Engineering →
Cyclical Time Encoding →
Regression Training →
6-Hour Forecast Generation
```

### Feature Engineering

The system generates:

- Hour-based cyclical features
- Day/night transformations
- Atmospheric trend vectors
- Rolling environmental averages

### Forecasting Characteristics

| Capability | Description |
|---|---|
| Forecast Horizon | 6 hours |
| Regression Model | HuberRegressor |
| Outlier Resistance | High |
| Small Dataset Handling | Automatic fallback logic |

---

<a id="visualization-layer"></a>

## 📊 Visualization Layer

### Plotly Operational Dashboards

The platform uses Plotly Graph Objects to build layered analytical weather visualizations.

Dashboard analytics include:

- Temperature vs feels-like trends
- Pressure overlays
- Humidity analytics
- Forecast projection lines
- Statistical anomaly markers
- Atmospheric variability tracking

### 3D Atmospheric Mapping

Pydeck powers immersive atmospheric visualization through:

- Spatial pressure intensity rendering
- Weather-driven elevation columns
- Environmental color scaling
- Multi-city atmospheric distribution
- Interactive geospatial exploration

---

<a id="dashboard-layer"></a>

## 🖥️ Dashboard Layer

The Streamlit dashboard acts as a centralized atmospheric operations console for analytical monitoring and environmental intelligence.

### Operational Dashboard Features

- Multi-city monitoring
- Historical trend analytics
- Forecast comparison dashboards
- Atmospheric anomaly visibility
- Real-time environmental KPIs
- Geospatial atmospheric intelligence

### UI Design Philosophy

- Dark SaaS-inspired interface
- Enterprise operational layout
- Recruiter-grade visual hierarchy
- Real-time analytical presentation
- Dashboard-driven workflow orchestration

---

<a id="project-structure"></a>

## 📁 Project Structure

```text
Weather-Forecast-Alert-Application/
|
|-- app.py
|-- main.py
|-- requirements.txt
|-- README.md
|-- LICENSE
|-- .env.example
|
|-- data/
|   |-- weather_warehouse.duckdb
|   |-- simulation.py
|   |-- sample_current_weather.json
|   `-- sample_forecast.json
|
|-- src/
|   |-- weather_suite/
|   |   |-- __init__.py
|   |   |-- config.py
|   |   |-- engine.py
|   |   |-- analytics.py
|   |   `-- visualizations.py
|   |
|   |-- api_handler.py
|   |-- data_parser.py
|   |-- alert_system.py
|   `-- visualizer.py
|
|-- screenshots/
|   |-- dashboard.png
|   |-- anomalies.png
|   `-- atmospheric_map.png
|
`-- docs/
    |-- architecture.md
    `-- forecasting_pipeline.md
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

Copy `.env.example` into `.env`

```powershell
copy .env.example .env
```

Configure operational environment settings:

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

### Run via Local Virtual Environment

```powershell
.\.venv\Scripts\streamlit.exe run app.py
```

### Execute Legacy CLI Weather Workflow

```powershell
python main.py
```

The dashboard enables users to:

- Fetch live atmospheric data
- Persist weather observations
- Detect anomalies
- Generate weather forecasts
- Explore 3D atmospheric maps
- Analyze environmental trends

---

<a id="screenshots--outputs"></a>

## 🖼️ Screenshots & Outputs

<div align="center">

### Operational Dashboard

<img src="screenshots/dashboard.png" width="90%"/>

<br/><br/>

### Atmospheric Anomaly Analytics

<img src="screenshots/anomalies.png" width="90%"/>

<br/><br/>

### 3D Atmospheric Visualization

<img src="screenshots/atmospheric_map.png" width="90%"/>

</div>

### Example Operational Metrics

```text
🌦️ Weather Operations Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Cities Monitored        : 12
Anomalies Detected      : 4
Forecast Horizon        : 6 Hours
Database Records        : 18,420
Top Pressure Drop       : -12.8 hPa
Atmospheric Risk Level  : MODERATE
```

---

<a id="verification-performed"></a>

## ✅ Verification Performed

- Python modules validated successfully
- `py_compile` execution completed
- DuckDB persistence smoke tests passed
- Time-series analytical queries validated
- Forecast generation workflow verified
- Streamlit dashboard launched successfully
- OpenWeatherMap API integration tested
- Local HTTP response returned status `200`
- Plotly visualizations rendered successfully
- Pydeck geospatial layers validated
- Historical weather persistence confirmed

---

<a id="security--reliability"></a>

## 🔐 Security & Reliability

### Operational Safety Controls

- Environment-based API credential isolation
- Deterministic weather record handling
- Structured JSON payload normalization
- Safe fallback forecasting workflows
- Robust anomaly threshold enforcement

### Recommended Best Practices

- Never commit `.env` credentials
- Rotate API keys periodically
- Archive long-term weather datasets
- Monitor DuckDB storage growth
- Validate atmospheric payload integrity

---

<a id="learning-outcomes"></a>

## 🎓 Learning Outcomes

### Data Engineering

- DuckDB analytical warehousing
- Environmental ETL pipelines
- Indexed time-series querying
- Persistent atmospheric storage

### Machine Learning & Analytics

- Regression forecasting workflows
- Statistical anomaly detection
- Time-based feature engineering
- Atmospheric intelligence modeling

### Visualization Engineering

- Plotly operational dashboarding
- Pydeck geospatial rendering
- Multi-layer atmospheric visualization
- Real-time analytical dashboards

### Software Architecture

- Service-oriented design patterns
- Modular analytics architecture
- Streamlit operations dashboarding
- Environment-driven configuration management

### Operational Intelligence

- Atmospheric monitoring workflows
- Forecast interpretation systems
- Environmental KPI analytics
- Geospatial operational visualization

---

<a id="future-improvements"></a>

## 🔮 Future Improvements

- [ ] Kafka-based streaming ingestion
- [ ] Real-time atmospheric event processing
- [ ] LSTM forecasting architecture
- [ ] FastAPI REST service layer
- [ ] Docker containerization
- [ ] Kubernetes deployment support
- [ ] Multi-region weather clustering
- [ ] Severe weather push notifications
- [ ] Historical climate trend analytics
- [ ] Satellite imagery integration
- [ ] Automated anomaly alerting engine
- [ ] Distributed environmental warehousing

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

[![GitHub stars](https://img.shields.io/github/stars/CH-S-K-CHAITANYA/Weather-Forecast-Alert-Application?style=social)](https://github.com/CH-S-K-CHAITANYA/Weather-Forecast-Alert-Application)

<br/>

⭐ If you found this project useful, consider starring the repository.

</div>

---
