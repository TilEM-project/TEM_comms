from pigeon import BaseMessage
from typing import Optional, List, Tuple, Mapping
from pydantic import model_validator


class Calibrate(BaseMessage):
    position: int
    image_shift: Tuple[int, int]


class Status(BaseMessage):
    enabled: bool
    current_position: Optional[int] = None
    image_shift: Tuple[int, int]
    calibration: Mapping[int, Calibrate]

    @model_validator(mode="after")
    def check_current_position(self):
        assert self.enabled == (self.current_position is not None)
        return self


class Command(BaseMessage):
    enable: bool
    position: Optional[int] = None

    @model_validator(mode="after")
    def check_position(self):
        assert self.enable == (self.position is not None)
        return self
