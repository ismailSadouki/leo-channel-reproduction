import pandas as pd

from incidence import elevation_azimuth_to_incidence

df = pd.read_csv("reports/pass_data.csv")

row = df.iloc[100]

direction = elevation_azimuth_to_incidence(
    row["elevation_deg"],
    row["azimuth_deg"],
)

print("Elevation:", row["elevation_deg"])
print("Azimuth:", row["azimuth_deg"])
print("Incidence:", direction)
print("Norm:", (direction ** 2).sum() ** 0.5)