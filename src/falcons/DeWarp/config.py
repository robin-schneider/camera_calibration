import dataclasses
import os
from typing import Optional, Tuple

import yaml


@dataclasses.dataclass
class DeWarpConfig:
    # Config Default Variables - Enter their values according to your Checkerboard, normal 64 (8x8) -1 inner corners only
    no_of_columns: int  # number of columns of your Checkerboard
    no_of_rows: int  # number of rows of your Checkerboard
    square_size: float  # size of square on the Checkerboard in mm -> TODO: This is no longer required?
    min_cap: int  # minimum or images to be collected by capturing (Default is 10), minimum is 3

    # Assuming the soccer field is 22 x 14 meters - old
    soccer_field_width: float
    soccer_field_length: float

    # Field Size and other dimensions for MSL field defaults see `falcon_config.yaml`
    field_length: float  # meters
    field_width: float  # meters
    penalty_area_length: float  # E, meters
    penalty_area_width: float  # C, meters
    goal_area_length: float  # F, meters
    goal_area_width: float  # D, meters
    center_circle_radius: float  # H, meters
    spot_radius: float
    goal_depth: float  # Goal depth,
    goal_width: float  # Goal width 2m for this field -> 2.4m allowed?
    line_width: float  # K, meters
    ppm: int  # pixels per meter
    safe_zone: float  # Safety zone around the field, meters

    ### Total Field Size
    field_length_total: float = dataclasses.field(
        init=False
    )  # field_length + 2 * safe_zone  -- Adding safety zone to the length
    field_width_total: float = dataclasses.field(
        init=False
    )  # field_width + 2 * safe_zone  -- Adding safety zone to the width

    ### Landmarks
    # For 18 x 12 meter Field -- Falcon defaults
    # TODO Should the landmarks be
    # 1) read from config or
    # 2) inferred from `field_width` and `center_circle_radius` --- current setting
    # Landmark 1, where the middle circle meets the middle line
    landmark1: Tuple[float, float] = dataclasses.field(init=False)
    # Landmark 2, where the middle line meets the outer field line
    landmark2: Tuple[float, float] = dataclasses.field(init=False)
    # Landmark 3, from the center circle spot towards the goal, where the (fictive) line meets the center circle line
    landmark3: Tuple[float, float] = dataclasses.field(init=False)
    # Landmark 4, Penalty Spot
    landmark4: Tuple[float, float] = dataclasses.field(init=False)

    field_coordinates_center: Tuple[int, int] = dataclasses.field(init=False)
    field_coordinates_lm1: Tuple[int, int] = dataclasses.field(init=False)
    field_coordinates_lm2: Tuple[int, int] = dataclasses.field(init=False)
    field_coordinates_lm3: Tuple[int, int] = dataclasses.field(init=False)
    field_coordinates_lm4: Tuple[int, int] = dataclasses.field(init=False)

    def __post_init__(self):
        self.field_length_total = self.field_length + 2 * self.safe_zone
        self.field_width_total = self.field_width + 2 * self.safe_zone
        self.field_coordinates_center = (
            int(self.field_length_total / 2) * self.ppm,
            int(self.field_width_total / 2) * self.ppm,
        )

        self.landmark1 = (self.center_circle_radius, 0)
        self.landmark2 = (self.field_width / 2, 0)
        self.landmark3 = (0, self.center_circle_radius)
        self.landmark4 = (0, self.field_width / 2)

        # TODO Why are the x-y coordinates flipped wrt to the landmarks?
        self.field_coordinates_lm1 = (
            int((self.field_length_total / 2 - self.landmark1[1]) * self.ppm),
            int((self.field_width_total / 2 - self.landmark1[0]) * self.ppm),
        )
        self.field_coordinates_lm2 = (
            int((self.field_length_total / 2 - self.landmark2[1]) * self.ppm),
            int((self.field_width_total / 2 - self.landmark2[0]) * self.ppm),
        )
        self.field_coordinates_lm3 = (
            int((self.field_length_total / 2 - self.landmark3[1]) * self.ppm),
            int((self.field_width_total / 2 - self.landmark3[0]) * self.ppm),
        )
        self.field_coordinates_lm4 = (
            int((self.field_length_total / 2 - self.landmark4[1]) * self.ppm),
            int((self.field_width_total / 2 - self.landmark4[0]) * self.ppm),
        )


def get_config(path_to_config: Optional[str] = None) -> DeWarpConfig:
    """Takes a str to a `.yaml` or if `None` loads the default Falcon config."""
    if not path_to_config:
        path_to_config = os.path.join(os.path.dirname(__file__), "falcon_config.yaml")
    with open(path_to_config, "r") as f:
        config = yaml.safe_load(f)

    return DeWarpConfig(**config)
