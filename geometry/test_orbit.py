# from skyfield.api import load
# from pathlib import Path
# import sys
# sys.path.append(str(Path(__file__).parent.parent))


# from orbit import load_satellite, propagate


# satellite, ts = load_satellite(
#     "data/tle/starlink.txt"
# )

# # One time instant for now.
# times = ts.utc(2026, 9, 2, 20, 0, 0)

# positions, velocities = propagate(
#     satellite,
#     ts,
#     times,
# )

# print("Satellite:", satellite.name)
# print("Position [km]:", positions)
# print("Velocity [km/s]:", velocities)



from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from skyfield.api import load

from orbit import load_satellite
from coordinates import create_ground_station, compute_geometry


satellite, ts = load_satellite(
    "data/tle/starlink.txt"
)


ground_station = create_ground_station(
    # ts,
    latitude_deg=40.7128,
    longitude_deg=-74.0060,
    height_m=10.0,
)




times = ts.utc(
    2026,
    9,
    2,
    20,
    0,
    0,
)




elevation, azimuth, range_km = compute_geometry(
    satellite,
    ground_station,
    times,
)


print("Satellite:", satellite.name)
print(f"Elevation: {elevation:.3f} deg")
print(f"Azimuth:   {azimuth:.3f} deg")
print(f"Range:     {range_km:.3f} km")