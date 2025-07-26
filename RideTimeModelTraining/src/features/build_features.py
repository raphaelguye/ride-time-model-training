import pandas as pd

def build_feature_matrix(ride_data, weather_data):
    # Merge ride and weather data on date and location
    merged_data = pd.merge(ride_data, weather_data, on=['date', 'location'])

    # Select relevant features for the model
    feature_matrix = merged_data[['ride_id', 'date', 'start_hour', 'weekday', 
                                   'distance_km', 'elevation_gain', 
                                   'temperature', 'wind_speed', 'rain']]

    return feature_matrix

def main():
    # Load raw ride data
    ride_data = pd.read_csv('data/processed/ride_data.csv')  # Placeholder path
    # Load weather data
    weather_data = pd.read_csv('data/processed/weather_data.csv')  # Placeholder path

    # Build feature matrix
    features = build_feature_matrix(ride_data, weather_data)

    # Save the feature matrix to CSV
    features.to_csv('data/processed/features.csv', index=False)

if __name__ == "__main__":
    main()