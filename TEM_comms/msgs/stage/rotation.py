from ..base import BaseMessage

class command(BaseMessage):
    angle_x: float | None = None
    angle_y: float | None = None
    calibrate: bool = False

class status(BaseMessage):
    angle_x: float
    angle_y: float
    in_motion: bool
    error: str = ""