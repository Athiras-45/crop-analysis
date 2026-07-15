"""
weather.py
-----------
Fetches weather data from the Open-Meteo API.
"""

import requests


def get_weather(latitude, longitude):
    """Fetch current weather from Open-Meteo."""

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&current=temperature_2m,relative_humidity_2m,"
        "precipitation,wind_speed_10m,pressure_msl"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        current = data["current"]

        weather_data = {
            "Temperature": current["temperature_2m"],
            "Humidity": current["relative_humidity_2m"],
            "Rainfall": current["precipitation"],
            "Wind Speed": current["wind_speed_10m"],
            "Pressure": current["pressure_msl"]
        }

        return weather_data

    except requests.exceptions.RequestException as e:
        print(f"Unable to fetch weather data: {e}")
        return None

    except (KeyError, TypeError, ValueError) as e:
        print(f"Unexpected response format from weather API: {e}")
        return None
