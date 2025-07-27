import requests
import pandas as pd
from urllib.parse import urlencode

def fetch_weather_data(date, location):
    api_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 46.991,
        "longitude": 6.9293,
        "hourly": "temperature_2m,wind_speed_10m,precipitation",
        "timezone": "Europe/Zurich"
    }

    # Log the full API URL with parameters
    full_url = f"{api_url}?{urlencode(params)}"
    print(f"Requesting weather data from: {full_url}")

    response = requests.get(api_url, params=params)
    print(response.json())

    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        raise Exception(f"Error fetching weather data: {response.status_code}")

def process_weather_data(weather_data):
    # Extract relevant weather information
    temperature = weather_data['hourly']['temperature_2m']
    wind_speed = weather_data['hourly']['wind_speed_10m']
    rain = [precip > 0 for precip in weather_data['hourly']['precipitation']]

    return pd.DataFrame({
        'temperature': temperature,
        'wind_speed': wind_speed,
        'rain': rain
    })

def main():
    # Example usage
    date = "2025-01-01"
    location = {'lat': 46.9910, 'lon': 6.9293}
    weather_data = fetch_weather_data(date, location)
    processed_data = process_weather_data(weather_data)
    print(processed_data)

if __name__ == "__main__":
    main()