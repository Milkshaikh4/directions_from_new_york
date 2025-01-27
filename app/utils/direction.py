from geographiclib.geodesic import Geodesic

def calculate_direction(latitude, longitude):
    ny_lat, ny_lon = 40.7128, -74.0060 
    geod = Geodesic.WGS84

    results = geod.Inverse(ny_lat, ny_lon, latitude, longitude) 

    azimuth = results['azi1'] 

    if 0 <= azimuth < 90:
        direction = "NE"
    elif 90 <= azimuth < 180:
        direction = "SE"
    elif 180 <= azimuth < 270:
        direction = "SW"
    else:
        direction = "NW"

    return direction