from ..base import BaseMessage

class command(BaseMessage):
    x: int | None = None
    y: int | None = None
    calibrate: bool = False

class status(BaseMessage):
    x: int
    y: int
    in_motion: bool
    error: str = ""