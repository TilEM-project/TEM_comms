from pigeon import BaseMessage
from pydantic import ConfigDict, Field


class Command(BaseMessage):
    """
    This message is uesd to change between apertures on a substrate.
    """

    model_config = ConfigDict(extra="allow")

    aperture_id: int | None = Field(
        default=None,
        description="The ID of the aperture to change to, or None to remain at the current aperture.",
    )
    calibrate: bool = Field(
        default=False,
        description="Set to True to initiate aperture changing hardware calibration.",
    )


class Status(BaseMessage):
    """
    This message includes status information about the aperture changing system.
    """

    model_config = ConfigDict(extra="allow")

    current_aperture: int | None = Field(
        description="The ID of the current aperture, or None if unknown."
    )
    calibrated: bool = Field(
        description="True if the aperture changing hardware is calibrated."
    )
    error: str = Field(default="", description="An optional error message.")
