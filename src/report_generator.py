"""
Report Generator - Saves weather data and alerts as CSV files
"""

import os
import pandas as pd
from datetime import datetime

os.makedirs("reports", exist_ok=True)


def save_report(current: dict, forecast_df: pd.DataFrame, alerts: list) -> str:
    """
    Save complete weather report as CSV.
    Returns file path of saved report.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"reports/weather_report_{timestamp}.csv"

    # Build current weather section
    current_section = pd.DataFrame([{
        "Report Type":   "Current Weather",
        "City":          current["city"],
        "Country":       current["country"],
        "Temperature":   f"{current['temp']}°C",
        "Feels Like":    f"{current['feels_like']}°C",
        "Humidity":      f"{current['humidity']}%",
        "Wind Speed":    f"{current['wind_speed']} km/h",
        "Condition":     current["description"],
        "Visibility":    f"{current['visibility']} km",
        "Report Time":   current["timestamp"],
    }])

    # Build alerts section
    alerts_section = pd.DataFrame({
        "Report Type": ["Alert"] * len(alerts) if alerts else ["No Alerts"],
        "Alert Message": alerts if alerts else ["All weather conditions are within safe limits."]
    })

    # Save current weather
    current_section.to_csv(filename, index=False, mode="w")

    # Append a blank line separator
    with open(filename, "a") as f:
        f.write("\n")

    # Append alerts
    alerts_section.to_csv(filename, index=False, mode="a")

    # Append blank line
    with open(filename, "a") as f:
        f.write("\n")

    # Append forecast
    if not forecast_df.empty:
        forecast_df.to_csv(filename, index=False, mode="a")

    return filename