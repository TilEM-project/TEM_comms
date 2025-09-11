from pigeon import BaseMessage
from typing import Mapping
from pydantic import Field


class _Resolution(BaseMessage):
    nm_per_px: tuple[float, float] = Field(
        description="The X-Y size of each pixel in the processed camera image in nanometers.",
        examples=[(3.97, 4.03)],
    )
    rotation: float = Field(
        description="The rotation required to match a right-handed image coordinate system to the coordinate system of the stage in radians."
    )


class Resolution(BaseMessage):
    """
    This message contains the resolutions of all the calibrated magnifications of the microscope.
    """

    lowmag: Mapping[int, _Resolution] = Field(
        description="A mapping of calibrated low-mag magnifications to thier calibration values."
    )
    mag: Mapping[int, _Resolution] = Field(
        description="A mapping of calibrated high-mag magnifications to their calibration values."
    )


class Centroid(BaseMessage):
    """
    This message contains the location of the centroid of the specified aperture.
    """

    aperture_id: int = Field(
        description="The ID of the aperture that this centroid pertains to."
    )
    x: int = Field(
        description="The stage coordinate system X axis location of the centroid."
    )
    y: int = Field(
        description="The stage coordinate system Y axis location of the centroid."
    )
