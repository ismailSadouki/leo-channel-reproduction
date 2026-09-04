
from skyfield.api import wgs84

def create_ground_station(
        latitude_deg: float,
        longitude_deg: float,
        height_m: float
):
    """
    Create a ground station using WGS84 geodetic coordinates.
    """

    return wgs84.latlon(
        latitude_deg,
        longitude_deg,
        elevation_m=height_m
    )



def compute_geometry(satellite, ground_station, times):
    """
    Compute satellite geometry as seen from the ground station.

    Returns
    -------
    elevation_deg : ndarray
    azimuth_deg : ndarray
    range_km : ndarray
    """
    difference = satellite - ground_station

    topocentric = difference.at(times)

    elevation, azimuth, distance = (
        topocentric.altaz()
    )


    return (
        elevation.degrees,
        azimuth.degrees,
        distance.km
    )