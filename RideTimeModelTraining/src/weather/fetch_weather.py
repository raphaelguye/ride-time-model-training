import requests
import pandas as pd

def fetch_weather_data(date, location):
    # Replace with actual API endpoint and parameters
    api_url = f"https://api.open-meteo.com/v1/forecast?latitude={location['lat']}&longitude={location['lon']}&hourly=temperature_2m,precipitation_sum,wind_speed_10m"
    
    response = requests.get(api_url)
    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        raise Exception(f"Error fetching weather data: {response.status_code}")

def process_weather_data(weather_data):
    # Extract relevant weather information
    temperature = weather_data['hourly']['temperature_2m']
    wind_speed = weather_data['hourly']['wind_speed_10m']
    rain = [precip > 0 for precips in weather_data['hourly']['precipitation_sum']]
    
    return pd.DataFrame({
        'temperature': temperature,
        'wind_speed': wind_speed,
        'rain': rain
    })

def main():
    # Example usage
    date = "2023-10-01"
    location = {'lat': 40.7128, 'lon': -74.0060}  # Example coordinates for New York City
    weather_data = fetch_weather_data(date, location)
    processed_data = process_weather_data(weather_data)
    print(processed_data)

if __name__ == "__main__":
    main()