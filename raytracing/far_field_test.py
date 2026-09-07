import numpy as np

from incidence import elevation_azimuth_to_incidence


def equivalent_source_position(
    scene_center: np.ndarray,
    incidence_direction: np.ndarray,
    distance_m: float,
) -> np.ndarray:
    """
    Place an equivalent transmitter opposite to the propagation direction.

    incidence_direction:
        Direction of wave propagation, i.e. satellite -> scene.

    The source therefore lies in the opposite direction.
    """
    incidence_direction = np.asarray(incidence_direction, dtype=float)
    incidence_direction /= np.linalg.norm(incidence_direction)

    return scene_center - distance_m * incidence_direction



# "If I am at source and want to point a ray at target, which direction should the ray travel?"
def direction_from_source(
    source: np.ndarray, # position of the fake transmitter
    target: np.ndarray, # some point you want the ray to reach
) -> np.ndarray:
    """Unit direction from source toward target."""
    d = target - source
    return d / np.linalg.norm(d)



# Example M1 geometry
elevation_deg = 10.0
azimuth_deg = 90.0

incidence = elevation_azimuth_to_incidence(
    elevation_deg,
    azimuth_deg,
)

scene_center = np.array([0.0, 0.0, 0.0])

# Example M1 geometry
elevation_deg = 10.0
azimuth_deg = 90.0

incidence = elevation_azimuth_to_incidence(
    elevation_deg,
    azimuth_deg,
)

scene_center = np.array([0.0, 0.0, 0.0])

# Points spanning our ~100 m scene
test_points = np.array([
    [-50.0, -50.0, 0.0],
    [ 50.0, -50.0, 0.0],
    [-50.0,  50.0, 0.0],
    [ 50.0,  50.0, 0.0],
    [  0.0,   0.0, 0.0],
])


print("Incidence direction:", incidence)
print()



for distance_m in [10_000, 20_000, 50_000, 100_000]:
    source = equivalent_source_position(
        scene_center,
        incidence,
        distance_m,
    )

    angles = []

    for point in test_points:
        ray_direction = direction_from_source(source, point)

        # Angular difference from the desired plane-wave direction
        cosine = np.clip(
            np.dot(ray_direction, incidence),
            -1.0,
            1.0,
        )

        angle_deg = np.degrees(np.arccos(cosine))
        angles.append(angle_deg)

    print(f"Distance: {distance_m:>6} m")
    print(f"  max angular deviation: {max(angles):.6f} deg")
    print(f"  source position: {source}")
    print()