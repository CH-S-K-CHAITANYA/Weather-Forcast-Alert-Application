"""
Data Parser - Extracts and cleans weather data from API JSON responses
"""

import pandas as pd
from datetime import datetime


def parse_current_weather(data: dict) -> dict:
    """
    Parse current weather JSON response.
    Returns clean dictionary with all required fields.
    """
    return {
        "city":        data.get("name", "Unknown"),
        "country":     data.get("sys", {}).get("country", ""),
        "temp":        round(data["main"]["temp"], 1),
        "feels_like":  round(data["main"]["feels_like"], 1),
        "temp_min":    round(data["main"]["temp_min"], 1),
        "temp_max":    round(data["main"]["temp_max"], 1),
        "humidity":    data["main"]["humidity"],
        "pressure":    data["main"]["pressure"],
        "wind_speed":  round(data["wind"]["speed"] * 3.6, 1),  # m/s → km/h
        "wind_dir":    data["wind"].get("deg", 0),
        "description": data["weather"][0]["description"],
        "condition_id":data["weather"][0]["id"],
        "visibility":  round(data.get("visibility", 0) / 1000, 1),  # m → km
        "timestamp":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "rain_1h":     data.get("rain", {}).get("1h", 0),
    }


def parse_forecast(data: dict) -> pd.DataFrame:
    """
    Parse 5-day forecast JSON response.
    Returns Pandas DataFrame with one row per 3-hour interval.
    """
    if not data or "list" not in data:
        return pd.DataFrame()

    records = []
    for item in data["list"]:
        records.append({
            "datetime":    item["dt_txt"],
            "temp":        round(item["main"]["temp"], 1),
            "feels_like":  round(item["main"]["feels_like"], 1),
            "humidity":    item["main"]["humidity"],
            "wind_speed":  round(item["wind"]["speed"] * 3.6, 1),
            "description": item["weather"][0]["description"],
            "rain_prob":   round(item.get("pop", 0) * 100, 1),  # probability of precipitation
        })

    df = pd.DataFrame(records)
    df["datetime"] = pd.to_datetime(df["datetime"])
    return df