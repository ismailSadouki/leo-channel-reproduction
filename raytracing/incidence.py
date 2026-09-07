import numpy as np


def elevation_azimuth_to_incidence(
    elevation_deg: float,
    azimuth_deg: float,
) -> np.ndarray:
    """
    Convert local ENU elevation/azimuth into a unit vector
    pointing from the satellite toward the receiver/scene.

    Convention:
        x = East
        y = North
        z = Up

    Elevation:
        0 deg = horizon
        90 deg = zenith

    Azimuth:
        0 deg = North
        90 deg = East
    """

    elevation = np.deg2rad(elevation_deg)
    azimuth = np.deg2rad(azimuth_deg)

    # Receiver -> satellite
    direction_to_satellite = np.array([
        np.cos(elevation) * np.sin(azimuth),
        np.cos(elevation) * np.cos(azimuth),
        np.sin(elevation),
    ])

    # Satellite -> receiver
    incidence = -direction_to_satellite

    # Numerical safety: normalize
    incidence /= np.linalg.norm(incidence)

    return incidence









