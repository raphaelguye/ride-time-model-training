import gpxpy
import os

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
    gpx_files = [f for f in os.listdir('data/raw') if f.endswith('.gpx')]
    for gpx_file in gpx_files:
        metadata = parse_gpx(os.path.join('data/raw', gpx_file))
        metadata['ride_id'] = gpx_file  # Use filename as ride_id
        metadata['date'] = metadata['timestamps'][0].date() if metadata['timestamps'] else None
        metadata['start_hour'] = metadata['timestamps'][0].hour if metadata['timestamps'] else None
        metadata['weekday'] = metadata['timestamps'][0].weekday() if metadata['timestamps'] else None
        ride_data.append(metadata)

    # Convert to DataFrame and save to CSV
    import pandas as pd
    ride_data_df = pd.DataFrame(ride_data)
    ride_data_df.drop(columns=['timestamps'], inplace=True)  # Drop timestamps column for simplicity
    os.makedirs('data/processed', exist_ok=True)
    ride_data_df.to_csv('data/processed/ride_data.csv', index=False)
    print("Saved ride data to data/processed/ride_data.csv")