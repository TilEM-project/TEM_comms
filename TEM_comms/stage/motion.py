from typing import Optional
from pigeon import BaseMessage
from pydantic import ConfigDict, Field


class Command(BaseMessage):
    """
    This message is used to specify how the stage should move the sample.
    """

    model_config = ConfigDict(extra="allow")

    x: int | None = Field(
        default=None,
        description="The desired absolute X position of the stage in nanometers, or None to keep the current position.",
    )
    y: int | None = Field(
        default=None,
        description="The desired absolute Y position of the stage in nanometers, or None to keep the current position.",
    )
    z: Optional[int] = Field(
        default=None,
        description="The desired absolute Z position of the stage in nanometers, or None to keep the current position.",
    )
    calibrate: bool = Field(
        default=False, description="Set to True to initiate stage calibration."
    )


class Status(BaseMessage):
    """
    This message includes stage motion status information.
    """

    model_config = ConfigDict(extra="allow")

    x: int | None = Field(
        description="The current X position of the stage in nanometers, or None if unknown."
    )
    y: int | None = Field(
        description="The current Y position of the stage in nanometers, or None if unknown."
    )
    z: Optional[int] = Field(
        default=None,
        description="The current Z position of the stage in nanometers, or None if unknown.",
    )
    in_motion: bool = Field(
        description="This value is True if the stage is currently moving."
    )
    calibrated: bool = Field(description="True if the stage is calibrated.")
    error: str = Field(default="", description="An optional error message.")
