from .base import BaseMessage
from typing import Literal
from pydantic import model_validator

class command(BaseMessage):
    focus: int | None = None
    aperture: Literal["lowmag", "highmag"] | None = None
    mag_mode: Literal["LM", "MAG1", "MAG2"] | None = None
    mag: int | None = None

    @model_validator(mode="after")
    @classmethod
    def check_mag(cls, data):
        assert (data.mag_mode is None) == (data.mag is None)
        return data


class status(BaseMessage):
    focus: int
    aperture: str | None
    mag_mode: str
    mag: int
    tank_voltage: int