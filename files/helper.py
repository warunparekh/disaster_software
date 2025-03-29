from nested_lookup import nested_lookup


def shrink_square(bbox, factor=0.5):
    lon_min, lon_max, lat_min, lat_max = bbox

    lon_center = (lon_min + lon_max) / 2
    lat_center = (lat_min + lat_max) / 2

    lon_range = lon_max - lon_min
    lat_range = lat_max - lat_min

    new_lon_range = lon_range * factor
    new_lat_range = lat_range * factor

    new_lon_min = lon_center - new_lon_range / 2
    new_lon_max = lon_center + new_lon_range / 2
    new_lat_min = lat_center - new_lat_range / 2
    new_lat_max = lat_center + new_lat_range / 2

    return [new_lon_min, new_lon_max, new_lat_min, new_lat_max]

def parse_thread(thread):
    """Parse a single thread item to extract relevant data"""

    return {
        "text": nested_lookup("text", thread),
        "username": nested_lookup("username", thread),
        "timestamp": nested_lookup("timestamp", thread),
    }