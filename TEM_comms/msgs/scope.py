from .base import BaseMessage
from typing import Literal
from pydantic import model_validator

class command(BaseMessage):
    focus: int | None = None
    mag_mode: Literal["LM", "MAG1", "MAG2"] | None = None
    mag: int | None = None

    @model_validator(mode="after")
    def check_mag(self):
        assert (self.mag_mode is None) == (self.mag is None)
        return self


class status(BaseMessage):
    focus: int
    aperture: str | None
    mag_mode: str
    mag: int
    tank_voltage: int