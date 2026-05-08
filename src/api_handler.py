"""
API Handler - Manages all HTTP requests to OpenWeatherMap API
"""

import requests

BASE_URL = "https://api.openweathermap.org/data/2.5"

def fetch_current_weather(city: str, api_key: str) -> dict | None:
    """
    Fetch current weather data for a given city.
    Returns parsed JSON dict or None if request fails.
    """
    url = f"{BASE_URL}/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"   # Use Celsius directly
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            print("❌ Invalid API Key. Check your .env file.")
        elif response.status_code == 404:
            print(f"❌ City '{city}' not found. Check spelling.")
        else:
            print(f"❌ API Error: {response.status_code} — {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ No internet connection.")
    except requests.exceptions.Timeout:
        print("❌ Request timed out. Try again.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

    return None


def fetch_forecast(city: str, api_key: str) -> dict | None:
    """
    Fetch 5-day / 3-hour forecast for a given city.
    Returns parsed JSON dict or None if request fails.
    """
    url = f"{BASE_URL}/forecast"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Forecast API Error: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Forecast fetch failed: {e}")

    return None