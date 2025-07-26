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

    for track in gpx.tracks:
        for segment in track.segments:
            total_distance += segment.length_3d()  # in meters
            points = segment.points
            for i in range(1, len(points)):
                elevation_diff = points[i].elevation - points[i - 1].elevation
                if elevation_diff > 0:  # Only count positive elevation changes
                    total_elevation_gain += elevation_diff
            timestamps.extend([point.time for point in points if point.time])

    return {
        'distance_km': total_distance / 1000,  # convert to kilometers
        'elevation_gain': total_elevation_gain,  # in meters
        'timestamps': timestamps
    }

if __name__ == "__main__":
    # Example usage
    gpx_files = [f for f in os.listdir('data/raw') if f.endswith('.gpx')]
    for gpx_file in gpx_files:
        metadata = parse_gpx(os.path.join('data/raw', gpx_file))
        print(f"Parsed {gpx_file}: {metadata}")