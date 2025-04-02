from typing import Optional
from pigeon import BaseMessage


class Command(BaseMessage):
    x: int | None = None
    y: int | None = None
    z: Optional[int] = None
    calibrate: bool = False


class Status(BaseMessage):
    x: int | None
    y: int | None
    z: Optional[int] = None
    in_motion: bool
    error: str = ""
