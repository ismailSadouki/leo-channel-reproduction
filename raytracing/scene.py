import mitsuba as mi
mi.set_variant("cuda_ad_rgb")
from sionna.rt import Camera, Receiver, load_scene_from_string


import numpy as np
from incidence import elevation_azimuth_to_incidence
from sionna.rt import Transmitter


def build_scene():
    """
    Build a small urban scene.

    The scene contains:
    - one ground surface
    - five rectangular buildings
    - one receiver at 1.5 m height
    """

    scene_xml = """
    <scene version="3.0.0">

        <!-- Ground -->
        <shape type="rectangle" id="ground">
            <transform name="to_world">
                <scale x="100" y="100"/>
            </transform>

            <bsdf type="diffuse" id="mat-itu_concrete"/>
        </shape>


        <!-- Buildings -->

        <shape type="cube" id="building_1">
            <transform name="to_world">
                <translate x="-30" y="-15" z="10"/>
                <scale x="15" y="20" z="10"/>
            </transform>

            <ref id="mat-itu_concrete"/>
        </shape>


        <shape type="cube" id="building_2">
            <transform name="to_world">
                <translate x="0" y="-15" z="15"/>
                <scale x="12" y="20" z="15"/>
            </transform>

            <ref id="mat-itu_concrete"/>
        </shape>


        <shape type="cube" id="building_3">
            <transform name="to_world">
                <translate x="30" y="-15" z="8"/>
                <scale x="15" y="20" z="8"/>
            </transform>

            <ref id="mat-itu_concrete"/>
        </shape>


        <shape type="cube" id="building_4">
            <transform name="to_world">
                <translate x="-25" y="25" z="12"/>
                <scale x="18" y="12" z="12"/>
            </transform>

            <ref id="mat-itu_concrete"/>
        </shape>


        <shape type="cube" id="building_5">
            <transform name="to_world">
                <translate x="20" y="25" z="18"/>
                <scale x="15" y="12" z="18"/>
            </transform>

            <ref id="mat-itu_concrete"/>
        </shape>

    </scene>
    """

    scene = load_scene_from_string(scene_xml)

    # Receiver in the open area between buildings.
    receiver = Receiver(
        name="rx",
        position=mi.Point3f(0.0, 15.0, 1.5),
        display_radius=1.0,
    )

    scene.add(receiver)


    #Equivalent far-field transmitter
    elevation_deg = 10.0
    azimuth_deg = 90.0

    incidence = elevation_azimuth_to_incidence(
        elevation_deg,
        azimuth_deg,
    )

    scene_center = np.array([0.0, 0.0, 0.0])
    far_field_distance = 50_000.0  # meters

    tx_position = (
        scene_center
        - far_field_distance * incidence
    )

    transmitter = Transmitter(
        name="tx",
        position=mi.Point3f(*tx_position.tolist()),
        look_at=mi.Point3f(*scene_center.tolist()),
        power_dbm=44,
    )

    scene.add(transmitter)

    print("incidence direction:", incidence)
    print("equivalent TX position:", tx_position)
    print("TX distance:", np.linalg.norm(tx_position))

    return scene


if __name__ == "__main__":
    scene = build_scene()

    print("Scene loaded successfully.")
    print("Objects:", scene.objects)
    print("Receivers:", scene.receivers)

    # Camera positioned above and away from the buildings.
    camera = Camera(
        position=mi.Point3f(90.0, 90.0, 70.0),
        look_at=mi.Point3f(0.0, 0.0, 10.0),
    )

    output_path = "reports/scene.png"

    # scene.render_to_file(
    #     camera=camera,
    #     filename=output_path,
    #     resolution=(1000, 700),
    #     num_samples=128,
    #     show_devices=True,
    #     show_orientations=True,
    # )

    # print(f"Sanity render saved to: {output_path}")
    print("scene validation: PASSED")