from pigeon import BaseMessage
from pydantic import Field


class Command(BaseMessage):
    """
    This message is used to rotate the sample, and to calibrate this rotation.
    """

    angle_x: float | None = Field(
        default=None,
        description="The desired rotation angle around the X axis in radians, or None to keep the current value.",
    )
    angle_y: float | None = Field(
        default=None,
        description="The desired rotation angle around the Y axis in radians, or None to keep the current value.",
    )
    eucentric_height: float | None = Field(
        default=None,
        description="The eucentric height of the stage in nanometers for calibration, or None to keep the current value.",
    )
    calibrate: bool = Field(
        default=False, description="If True, calibrate the sample rotation hardware."
    )


class Status(BaseMessage):
    """
    This message contains the status of the sample rotation system.
    """

    angle_x: float = Field(
        description="The current angle around the X axis in radians."
    )
    angle_y: float = Field(
        description="The current angle around the Y axis in radians."
    )
    eucentric_height: float = Field(
        description="The current enucentric height value in nanometers."
    )
    in_motion: bool = Field(
        description="True if the rotation stage is currently moving."
    )
    error: str = Field(default="", description="An optional error message.")
