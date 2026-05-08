"""
Alert System - Checks weather conditions against thresholds and generates alerts
"""


def check_alerts(current: dict, thresholds: dict) -> list:
    """
    Compare current weather values against alert thresholds.
    Returns list of alert message strings.
    """
    alerts = []

    temp = current.get("temp", 0)
    humidity = current.get("humidity", 0)
    wind_speed = current.get("wind_speed", 0)
    condition_id = current.get("condition_id", 800)
    rain_1h = current.get("rain_1h", 0)

    # 🌡️ High Temperature Alert
    if temp > thresholds["max_temp"]:
        alerts.append(
            f"HIGH TEMPERATURE ALERT: {temp}°C exceeds {thresholds['max_temp']}°C threshold. "
            f"Stay hydrated, avoid direct sunlight."
        )

    # ❄️ Cold / Frost Alert
    if temp < thresholds["min_temp"]:
        alerts.append(
            f"COLD WEATHER ALERT: {temp}°C is below {thresholds['min_temp']}°C. "
            f"Risk of frost. Protect crops and pipes."
        )

    # 💧 High Humidity Alert
    if humidity > thresholds["max_humidity"]:
        alerts.append(
            f"HIGH HUMIDITY ALERT: {humidity}% humidity (threshold: {thresholds['max_humidity']}%). "
            f"Risk of mold growth and heat stress."
        )

    # 🌪️ Storm / High Wind Alert
    if wind_speed > thresholds["max_wind"]:
        alerts.append(
            f"STORM ALERT: Wind speed {wind_speed} km/h exceeds {thresholds['max_wind']} km/h. "
            f"Avoid outdoor activities. Secure loose objects."
        )

    # 🌧️ Heavy Rain Alert (condition codes 500-531 = rain, 200-232 = thunderstorm)
    if 200 <= condition_id <= 531:
        alerts.append(
            f"RAIN/STORM ALERT: Current condition '{current.get('description', '')}'. "
            f"Carry umbrella. Avoid low-lying flood-prone areas."
        )

    # 🌧️ Rain accumulation alert
    if rain_1h > 10:
        alerts.append(
            f"HEAVY RAINFALL ALERT: {rain_1h}mm rain in last hour. "
            f"Risk of waterlogging and reduced visibility."
        )

    return alerts


def check_forecast_alerts(forecast_df, thresholds: dict) -> list:
    """
    Check forecast data for upcoming dangerous conditions.
    Returns list of forward-looking alert messages.
    """
    alerts = []

    if forecast_df.empty:
        return alerts

    # Check max temperature in forecast
    max_forecast_temp = forecast_df["temp"].max()
    if max_forecast_temp > thresholds["max_temp"]:
        peak_time = forecast_df.loc[forecast_df["temp"].idxmax(), "datetime"]
        alerts.append(
            f"FORECAST HEAT ALERT: Temperature expected to reach {max_forecast_temp}°C "
            f"around {peak_time}."
        )

    # Check max wind in forecast
    max_wind = forecast_df["wind_speed"].max()
    if max_wind > thresholds["max_wind"]:
        alerts.append(f"FORECAST STORM WARNING: Wind speeds up to {max_wind} km/h expected.")

    # Check rain probability
    if "rain_prob" in forecast_df.columns:
        max_rain_prob = forecast_df["rain_prob"].max()
        if max_rain_prob > thresholds["rain_probability"]:
            alerts.append(f"FORECAST RAIN ALERT: {max_rain_prob}% chance of precipitation expected.")

    return alerts