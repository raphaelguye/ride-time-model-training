import requests
import pandas as pd
from urllib.parse import urlencode
import os

def fetch_weather_data(date, location):
    api_url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
    params = {
        "latitude": location['lat'],
        "longitude": location['lon'],
        "start_date": date,
        "end_date": date,
        "timezone": "Europe/Zurich",
        "hourly": "temperature_2m,wind_speed_10m,precipitation",
    }

    # Log the full API URL with parameters
    full_url = f"{api_url}?{urlencode(params)}"
    print(f"Requesting weather data from: {full_url}")

    response = requests.get(api_url, params=params)
    # print(response.json())

    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        raise Exception(f"Error fetching weather data: {response.status_code}")

def process_weather_data(weather_data, target_hour=None):
    # Extract relevant weather information
    temperature = weather_data['hourly']['temperature_2m']
    wind_speed = weather_data['hourly']['wind_speed_10m']
    rain = [precip > 0 for precip in weather_data['hourly']['precipitation']]
    time = weather_data['hourly']['time']

    df = pd.DataFrame({
        'time': time,
        'temperature': temperature,
        'wind_speed': wind_speed,
        'rain': rain
    })

    if target_hour is not None:
        # target_hour should be a string like '14:00'
        df = df[df['time'].str.endswith(f"T{target_hour}")]
        df = df.reset_index(drop=True)
    return df

def main():
    # Example usage
    date = "2025-01-01"
    location = {'lat': 46.9910, 'lon': 6.9293}
    target_hour = "14:00"  # Set your desired hour here
    weather_data = fetch_weather_data(date, location)
    processed_data = process_weather_data(weather_data, target_hour=target_hour)
    print(processed_data)

    # # Add date and location columns
    # processed_data['date'] = date
    # processed_data['location'] = f"{location['lat']},{location['lon']}"

    # # Save to CSV
    # os.makedirs('data/processed', exist_ok=True)
    # processed_data.to_csv('data/processed/weather_data.csv', index=False)
    # print("Saved weather data to data/processed/weather_data.csv")

if __name__ == "__main__":
    main()