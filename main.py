"""
Weather Forecast & Alert Application
Main entry point - runs both API and simulation modes
"""

import os
import sys
from dotenv import load_dotenv
from src.api_handler import fetch_current_weather, fetch_forecast
from src.data_parser import parse_current_weather, parse_forecast
from src.alert_system import check_alerts
from src.visualizer import plot_temperature_trend, plot_humidity_chart
from src.report_generator import save_report
from data.simulation import get_simulated_data

# Load environment variables
load_dotenv()

# ============ CONFIGURATION ============
ALERT_THRESHOLDS = {
    "max_temp": 38,        # Celsius — high temperature alert
    "min_temp": 5,         # Celsius — cold alert
    "max_humidity": 85,    # Percent — humidity alert
    "max_wind": 50,        # km/h — storm alert
    "rain_probability": 70 # Percent — rain alert
}

def run_api_mode(city: str):
    """Fetch live data from OpenWeatherMap API."""
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        print("❌ ERROR: WEATHER_API_KEY not found in .env file.")
        sys.exit(1)

    print(f"\n🌍 Fetching live weather data for: {city}")
    print("=" * 50)

    # Fetch current weather
    raw_current = fetch_current_weather(city, api_key)
    if not raw_current:
        print("❌ Could not fetch weather data. Check city name or API key.")
        return

    current = parse_current_weather(raw_current)

    # Fetch 5-day forecast
    raw_forecast = fetch_forecast(city, api_key)
    forecast_df = parse_forecast(raw_forecast)

    return current, forecast_df


def run_simulation_mode():
    """Use local sample data (no API key needed)."""
    print("\n🔬 Running in SIMULATION MODE (using sample data)")
    print("=" * 50)
    current, forecast_df = get_simulated_data()
    return current, forecast_df


def display_weather(current: dict):
    """Print current weather to terminal."""
    print("\n📍 CURRENT WEATHER REPORT")
    print("-" * 40)
    print(f"🏙️  City:         {current['city']}")
    print(f"🌡️  Temperature:  {current['temp']}°C  (Feels like {current['feels_like']}°C)")
    print(f"💧  Humidity:     {current['humidity']}%")
    print(f"🌬️  Wind Speed:   {current['wind_speed']} km/h")
    print(f"☁️  Condition:    {current['description'].title()}")
    print(f"👁️  Visibility:   {current['visibility']} km")
    print("-" * 40)


def display_alerts(alerts: list):
    """Print alert messages to terminal."""
    print("\n🚨 ALERT SYSTEM")
    print("-" * 40)
    if alerts:
        for alert in alerts:
            print(f"  ⚠️  {alert}")
    else:
        print("  ✅ No alerts. Weather conditions are normal.")
    print("-" * 40)


def main():
    print("\n" + "🌦️" * 20)
    print("   WEATHER FORECAST & ALERT APPLICATION")
    print("🌦️" * 20)

    # Choose mode
    print("\nSelect Mode:")
    print("  [1] API Mode (Live data — requires API key)")
    print("  [2] Simulation Mode (Sample data — no API key needed)")

    choice = input("\nEnter choice (1 or 2): ").strip()

    if choice == "1":
        city = input("Enter city name: ").strip()
        result = run_api_mode(city)
    elif choice == "2":
        result = run_simulation_mode()
    else:
        print("Invalid choice. Running simulation mode.")
        result = run_simulation_mode()

    if not result:
        return

    current, forecast_df = result

    # Display current weather
    display_weather(current)

    # Check and display alerts
    alerts = check_alerts(current, ALERT_THRESHOLDS)
    display_alerts(alerts)

    # Show forecast
    print("\n📅 5-DAY FORECAST SUMMARY")
    print("-" * 40)
    print(forecast_df[["datetime", "temp", "humidity", "description"]].to_string(index=False))
    print("-" * 40)

    # Generate visualizations
    print("\n📊 Generating Charts...")
    plot_temperature_trend(forecast_df, current["city"])
    plot_humidity_chart(forecast_df, current["city"])
    print("  ✅ Charts saved to outputs/ folder")

    # Save report
    print("\n📄 Saving Report...")
    report_path = save_report(current, forecast_df, alerts)
    print(f"  ✅ Report saved: {report_path}")

    print("\n✅ Application completed successfully!")
    print("🌦️" * 20 + "\n")


if __name__ == "__main__":
    main()