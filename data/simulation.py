"""
Simulation Mode - Provides sample weather data when API key is unavailable.
Perfect for testing and demonstration without internet or API key.
"""

import pandas as pd
from datetime import datetime, timedelta


def get_simulated_data():
    """
    Returns simulated current weather + forecast DataFrame.
    Simulates Mumbai weather with a storm scenario (triggers multiple alerts).
    """

    # Simulated current weather — triggers alerts!
    current = {
        "city":         "Mumbai (Simulated)",
        "country":      "IN",
        "temp":         39.5,       # Triggers heat alert (> 38°C)
        "feels_like":   44.2,
        "temp_min":     35.0,
        "temp_max":     40.1,
        "humidity":     88,         # Triggers humidity alert (> 85%)
        "pressure":     1005,
        "wind_speed":   55.0,       # Triggers storm alert (> 50 km/h)
        "wind_dir":     180,
        "description":  "heavy intensity rain",
        "condition_id": 502,        # Triggers rain alert (500-531)
        "visibility":   2.5,
        "timestamp":    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "rain_1h":      12.5,       # Triggers heavy rainfall alert (> 10mm)
    }

    # Simulated 5-day forecast
    base_time = datetime.now().replace(minute=0, second=0, microsecond=0)
    forecast_records = []

    # Simulate realistic weather trend over 5 days (40 entries, 3h intervals)
    temps = [39.5, 40.1, 38.9, 37.2, 35.8, 34.5, 33.2, 32.0,
             31.5, 32.8, 34.1, 35.6, 36.2, 37.0, 38.5, 39.0,
             40.0, 40.5, 39.8, 38.2, 36.5, 35.0, 33.8, 32.5,
             31.0, 30.5, 31.5, 32.0, 33.5, 35.0, 36.5, 37.8,
             38.5, 39.2, 40.1, 38.9, 37.5, 36.0, 34.5, 33.0]

    humidities = [88, 90, 91, 89, 86, 82, 78, 75,
                  72, 70, 73, 76, 79, 82, 85, 87,
                  89, 91, 90, 88, 84, 80, 76, 72,
                  68, 65, 68, 72, 75, 78, 81, 84,
                  86, 88, 90, 87, 83, 79, 75, 70]

    conditions = ["heavy rain", "moderate rain", "heavy rain", "light rain",
                  "overcast", "cloudy", "partly cloudy", "clear sky",
                  "clear sky", "few clouds", "partly cloudy", "cloudy",
                  "overcast", "light rain", "moderate rain", "heavy rain",
                  "thunderstorm", "heavy rain", "moderate rain", "light rain",
                  "drizzle", "cloudy", "partly cloudy", "clear sky",
                  "clear sky", "sunny", "few clouds", "partly cloudy",
                  "cloudy", "overcast", "light rain", "moderate rain",
                  "heavy rain", "thunderstorm", "heavy rain", "moderate rain",
                  "light rain", "drizzle", "cloudy", "clear sky"]

    winds = [55, 58, 52, 45, 38, 30, 22, 18,
             15, 12, 14, 18, 22, 28, 35, 42,
             55, 60, 52, 40, 30, 22, 16, 12,
             10, 8, 10, 14, 18, 24, 30, 38,
             44, 52, 58, 48, 36, 26, 18, 12]

    rain_probs = [95, 90, 85, 70, 50, 30, 15, 5,
                  5, 5, 10, 20, 35, 50, 65, 80,
                  95, 95, 85, 70, 55, 35, 20, 10,
                  5, 5, 10, 20, 30, 45, 60, 75,
                  85, 95, 95, 80, 65, 45, 25, 10]

    for i in range(40):
        dt = base_time + timedelta(hours=i * 3)
        forecast_records.append({
            "datetime":    dt,
            "temp":        temps[i],
            "feels_like":  round(temps[i] + (humidities[i] - 60) * 0.1, 1),
            "humidity":    humidities[i],
            "wind_speed":  winds[i],
            "description": conditions[i],
            "rain_prob":   rain_probs[i],
        })

    forecast_df = pd.DataFrame(forecast_records)
    return current, forecast_df