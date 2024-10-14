from pigeon import BaseMessage
from typing import Literal, Optional, Tuple
from pydantic import model_validator


class Command(BaseMessage):
    focus: Optional[int] = None
    mag_mode: Optional[Literal["LM", "MAG1", "MAG2"]] = None
    mag: Optional[int] = None
    brightness: Optional[int] = None
    beam_offset: Optional[Tuple[int, int]] = None
    screen: Optional[Literal["up", "down"]] = None

    @model_validator(mode="after")
    def check_mag(self):
        assert (self.mag_mode is None) == (self.mag is None)
        return self


class Status(BaseMessage):
    focus: int
    aperture: str | None
    mag_mode: str
    mag: int
    tank_voltage: int
    brightness: int
    beam_offset: Tuple[int, int]
    screen: Literal["up", "down"] | None
