from pigeon import BaseMessage
from typing import Literal, Optional, Tuple
from pydantic import model_validator, Field
from . import image_shift


class Command(BaseMessage):
    """
    This message is used to change microscope settings.
    """

    focus: Optional[int] = Field(
        default=None,
        description="The desired focus value for the microscope, or None to keep the current value.",
    )
    mag_mode: Optional[Literal["LM", "MAG1", "MAG2"]] = Field(
        default=None,
        description="The desired magnification mode for the microscope, or None to keep the current value.",
    )
    mag: Optional[int] = Field(
        default=None,
        description="The desired magnification for the microscope, or None to keep the current value.",
    )
    brightness: Optional[int] = Field(
        default=None,
        description="The desired beam spread for the microscope, or None to keep the current value.",
    )
    beam_offset: Optional[Tuple[int, int]] = Field(
        default=None,
        description="The desired beam shift values, or None to keep the current value.",
    )
    spot_size: Optional[int] = Field(
        default=None,
        description="The desired spot size, or None to keep the current value.",
    )
    screen: Optional[Literal["up", "down"]] = Field(
        default=None,
        description='"up" to raise the microscope viewscreen, "down" to lower the microscope viewscreen, or None to keep the viewscreen in the current position.',
    )

    @model_validator(mode="after")
    def check_mag(self):
        assert (self.mag_mode is None) == (self.mag is None)
        return self


class Status(BaseMessage):
    """
    This message contains the state of the microscope.
    """

    focus: int = Field(description="The current focus value.")
    aperture: str | None = Field(
        description="The current status of the objective aperture, or None if unknown."
    )
    mag_mode: Literal["MAG", "LOWMAG"] = Field(
        description="The curreng magnification mode."
    )
    mag: int = Field(description="The current magnification.")
    tank_voltage: int = Field(
        description="The current voltage of the tank in kilo-volts."
    )
    brightness: int = Field(description="The current beam spread.")
    beam_offset: Tuple[int, int] = Field(description="The current beam shift values.")
    spot_size: int = Field(description="The current spot size.")
    screen: Literal["up", "down"] | None = Field(
        description='Whether the viewscreen is currently "up", "down", or None for an unknown position.'
    )
