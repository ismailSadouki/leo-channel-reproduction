import numpy as np
import csv

from orbit import load_satellite
from coordinates import create_ground_station, compute_geometry


satellite, ts = load_satellite(
    "data/tle/starlink.txt"
)

ground_station = create_ground_station(
    latitude_deg=40.7128,
    longitude_deg=-74.0060,
    height_m=10.0,
)


# --------------------------------------------------
# Find passes
# --------------------------------------------------

t0 = ts.utc(2026, 9, 2, 0, 0, 0)
t1 = ts.utc(2026, 9, 3, 0, 0, 0)

times, events = satellite.find_events(
    ground_station,
    t0,
    t1,
    altitude_degrees=0.0,
)


# --------------------------------------------------
# Select the 20:06 pass
# --------------------------------------------------

rise_time = times[18]
set_time = times[20]

print("Selected pass:")
print("Rise:", rise_time.utc_strftime("%Y-%m-%d %H:%M:%S"))
print("Set: ", set_time.utc_strftime("%Y-%m-%d %H:%M:%S"))


# --------------------------------------------------
# Create 1-second samples
# --------------------------------------------------

duration_seconds = int(
    (set_time.tt - rise_time.tt) * 86400
)

sample_seconds = np.arange(
    0,
    duration_seconds + 1,
    1,
)

pass_times = ts.tt_jd(
    rise_time.tt + sample_seconds / 86400
)


# --------------------------------------------------
# Compute geometry
# --------------------------------------------------

elevation, azimuth, range_km = compute_geometry(
    satellite,
    ground_station,
    pass_times,
)


# --------------------------------------------------
# Print results
# --------------------------------------------------

print()
print("Number of samples:", len(pass_times))
print(
    f"Maximum elevation: "
    f"{np.max(elevation):.3f} deg"
)
print(
    f"Minimum range: "
    f"{np.min(range_km):.3f} km"
)



import matplotlib.pyplot as plt
from pathlib import Path

# Create output directory
output_dir = Path("reports")
output_dir.mkdir(exist_ok=True)

time_seconds = sample_seconds


# --------------------------------------------------
# Elevation
# --------------------------------------------------

plt.figure(figsize=(10, 5))
plt.plot(time_seconds, elevation)

plt.xlabel("Time since rise [s]")
plt.ylabel("Elevation [deg]")
plt.title("Satellite Elevation During Pass")
plt.grid(True)

plt.tight_layout()
plt.savefig(output_dir / "elevation_pass.png", dpi=150)
plt.close()


# --------------------------------------------------
# Range
# --------------------------------------------------

plt.figure(figsize=(10, 5))
plt.plot(time_seconds, range_km)

plt.xlabel("Time since rise [s]")
plt.ylabel("Range [km]")
plt.title("Satellite Range During Pass")
plt.grid(True)

plt.tight_layout()
plt.savefig(output_dir / "range_pass.png", dpi=150)
plt.close()


# --------------------------------------------------
# Azimuth
# --------------------------------------------------

plt.figure(figsize=(10, 5))
plt.plot(time_seconds, azimuth)

plt.xlabel("Time since rise [s]")
plt.ylabel("Azimuth [deg]")
plt.title("Satellite Azimuth During Pass")
plt.grid(True)

plt.tight_layout()
plt.savefig(output_dir / "azimuth_pass.png", dpi=150)
plt.close()


print()
print("Plots saved to:")
print(output_dir / "elevation_pass.png")
print(output_dir / "range_pass.png")
print(output_dir / "azimuth_pass.png")




# Radial velocity

dt = 1.0  # seconds

radial_velocity = np.gradient(
    range_km,
    dt,
) # v_r ​km/s



fc = 2e9  # Hz
c = 299792.458  # km/s

doppler_hz = -(
    radial_velocity / c
) * fc # Hz







# Doppler plot

plt.figure(figsize=(10, 5))

plt.plot(time_seconds, doppler_hz)

plt.xlabel("Time since rise [s]")
plt.ylabel("Doppler shift [Hz]")
plt.title("LEO Satellite Doppler Shift")
plt.grid(True)

plt.tight_layout()

plt.savefig(
    output_dir / "doppler_pass.png",
    dpi=150,
)

plt.close()






# Save pass data

csv_path = output_dir / "pass_data.csv"

with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow([
        "time",
        "elevation_deg",
        "azimuth_deg",
        "range_km",
        "radial_velocity_km_s",
        "doppler_hz",
    ])

    for i in range(len(pass_times)):
        writer.writerow([
            pass_times[i].utc_strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            elevation[i],
            azimuth[i],
            range_km[i],
            radial_velocity[i],
            doppler_hz[i],
        ])

print("Pass data saved to:")
print(csv_path)




print()
print("Doppler configuration:")
print(f"Carrier frequency: {fc / 1e9:.1f} GHz")
print(f"Speed of light:    {c:.3f} km/s")

print()
print("Doppler results:")
print(f"Maximum Doppler: {np.max(doppler_hz):.2f} Hz")
print(f"Minimum Doppler: {np.min(doppler_hz):.2f} Hz")
print(f"Maximum |Doppler|: {np.max(np.abs(doppler_hz)):.2f} Hz")

print()
print("Radial velocity:")
print(f"Maximum: {np.max(radial_velocity):.3f} km/s")
print(f"Minimum: {np.min(radial_velocity):.3f} km/s")

print()
print("Pass data saved to:")
print(csv_path)