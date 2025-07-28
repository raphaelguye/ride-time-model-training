import gpxpy
import os
from src.weather.fetch_weather import fetch_weather

def parse_gpx(file_path):
    """
    Parses a GPX file to extract ride metadata including distance, elevation gain, and timestamps.

    Args:
        file_path (str): The path to the GPX file.

    Returns:
        dict: A dictionary containing ride metadata.
    """
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    total_distance = 0.0
    total_elevation_gain = 0.0
    timestamps = []
    start_location = None

    for track in gpx.tracks:
        for segment in track.segments:
            total_distance += segment.length_3d()  # in meters
            points = segment.points
            if points and start_location is None:
                start_location = f"{points[0].latitude},{points[0].longitude}"
            for i in range(1, len(points)):
                elevation_diff = points[i].elevation - points[i - 1].elevation
                if elevation_diff > 0:  # Only count positive elevation changes
                    total_elevation_gain += elevation_diff
            timestamps.extend([point.time for point in points if point.time])

    return {
        'distance_km': total_distance / 1000,  # convert to kilometers
        'elevation_gain': total_elevation_gain,  # in meters
        'timestamps': timestamps,
        'start_location': start_location
    }

if __name__ == "__main__":
    ride_data = []

    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
    gpx_dir = os.path.join(project_root, 'data', 'raw')
    print("Resolved GPX dir:", gpx_dir)
    gpx_files = [
        os.path.join(gpx_dir, f)
        for f in os.listdir(gpx_dir)
        if f.endswith('.gpx') and os.path.isfile(os.path.join(gpx_dir, f))
    ]
    print("GPX files:", gpx_files)

    for gpx_file in gpx_files:
        metadata = parse_gpx(os.path.join('data/raw', gpx_file))
        # metadata['ride_id'] = gpx_file  # Use filename as ride_id
        metadata['date'] = metadata['timestamps'][0].date() if metadata['timestamps'] else None
        metadata['start_hour'] = metadata['timestamps'][0].hour if metadata['timestamps'] else None
        metadata['weekday'] = metadata['timestamps'][0].weekday() if metadata['timestamps'] else None
        ride_data.append(metadata)

    # Fetch weather data for each ride and append it to the ride data
    ride_data.sort(key=lambda x: x['date'] if x['date'] is not None else '')
    for ride in ride_data:
        if ride['start_location']:
            lat, lon = map(float, ride['start_location'].split(','))
            location = {'lat': lat, 'lon': lon}
            date = ride['date'].isoformat() if ride['date'] else None
            hour = f"{ride['start_hour']:02d}:00" if ride['start_hour'] is not None else None
            if date and hour is not None:
                weather_data = fetch_weather(date, hour, location)
                if weather_data is not None:
                    ride.update({
                        'temperature': weather_data.get('temperature'),
                        'wind_speed': weather_data.get('wind_speed'),
                        'rain': weather_data.get('rain')
                    })
                else:
                    print(f"⚠️ Warning: No weather data for ride on {date} at hour {hour} at location {location}")
                    ride.update({'temperature': None, 'wind_speed': None, 'rain': None})
            else:
                ride.update({'temperature': None, 'wind_speed': None, 'rain': None})
        else:
            ride.update({'temperature': None, 'wind_speed': None, 'rain': None})

    # Convert to DataFrame and save to CSV
    import pandas as pd
    ride_data_df = pd.DataFrame(ride_data)
    ride_data_df.drop(columns=['timestamps'], inplace=True)  # Drop timestamps column for simplicity
    os.makedirs('data/processed', exist_ok=True)
    ride_data_df.to_csv('data/processed/ride_data.csv', index=False)
    print("Saved ride data to data/processed/ride_data.csv")