import requests
import pandas as pd
from urllib.parse import urlencode
import os

def _fetch_weather_data(date, location):
    api_url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
    params = {
        "latitude": location['lat'],
        "longitude": location['lon'],
        "start_date": date,
        "end_date": date,
        "timezone": "GMT",
        "hourly": "temperature_2m,wind_speed_10m,precipitation",
    }

    # Log the full API URL with parameters
    full_url = f"{api_url}?{urlencode(params)}"
    print(f"Requesting weather data from: {full_url}")

    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        raise Exception(f"Error fetching weather data: {response.status_code}")

def _process_weather_data(weather_data, target_hour=None):
    temperature = weather_data['hourly']['temperature_2m']
    wind_speed = weather_data['hourly']['wind_speed_10m']
    rain = [precip > 0 for precip in weather_data['hourly']['precipitation']]
    time = weather_data['hourly']['time']

    for t, temp, ws, r in zip(time, temperature, wind_speed, rain):
        if target_hour is None or t.endswith(f"T{target_hour}"):
            return {
                'time': t,
                'timezone': weather_data.get('timezone'),
                'temperature': temp,
                'wind_speed': ws,
                'rain': r
            }
    return None

def fetch_weather(date, hour, location):
    weather_data = _fetch_weather_data(date, location)
    return _process_weather_data(weather_data, target_hour=hour)

# Example usage for testing
if __name__ == "__main__":
    date = "2025-01-01"
    hour = "12:00"
    location = {'lat': 46.9910, 'lon': 6.9293}
    result = fetch_weather(date, hour, location)
    print(result)