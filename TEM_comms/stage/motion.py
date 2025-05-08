from typing import Optional
from pigeon import BaseMessage
from pydantic import ConfigDict


class Command(BaseMessage):
    model_config = ConfigDict(extra="allow")

    x: int | None = None
    y: int | None = None
    z: Optional[int] = None
    calibrate: bool = False


class Status(BaseMessage):
    model_config = ConfigDict(extra="allow")

    x: int | None
    y: int | None
    z: Optional[int] = None
    in_motion: bool
    error: str = ""
