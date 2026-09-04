from pathlib import Path


import numpy as np
from skyfield.api import EarthSatellite, load

def load_satellite(tle_path: str):
    """Load a satellite from a 3-line TLE file"""

    lines = Path(tle_path).read_text().strip().splitlines()

    if len(lines) != 3:
        raise ValueError(
            "TLE file must contain exactly 3 lines: "
            "name, line 1, line 2."
        )

    name = lines[0].strip()
    line1 = lines[1].strip()
    line2 = lines[2].strip()

    ts = load.timescale()
    satellite = EarthSatellite(
        line1,
        line2,
        name,
        ts
    )

    return satellite, ts

def propagate(satellite, ts, times):
    """
    Propagate the satellite at the supplied Skyfield times.

    Returns
    -------
    positions_km : ndarray, shape (N, 3)
        Satellite position in km.
    velocities_km_s : ndarray, shape (N, 3)
        Satellite velocity in km/s.
    """
    geocentric = satellite.at(times)

    positions_km = np.asarray(
        geocentric.position.km
    ).T

    velocities_km_s = np.asarray(
        geocentric.velocity.km_per_s
    ).T
    

    return positions_km, velocities_km_s