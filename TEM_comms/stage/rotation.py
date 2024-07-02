from pigeon import BaseMessage


class Command(BaseMessage):
    angle_x: float | None = None
    angle_y: float | None = None
    calibrate: bool = False


class Status(BaseMessage):
    angle_x: float
    angle_y: float
    in_motion: bool
    error: str = ""
