from pigeon import BaseMessage
from typing import Optional


class Command(BaseMessage):
    tile_id: str


class Image(BaseMessage):
    tile_id: str
    path: str


class Settings(BaseMessage):
    exposure: float | None = None
    gain: Optional[float] = None
    width: int | None = None
    height: int | None = None


class Status(BaseMessage):
    exposure: float
    gain: float
    width: int
    height: int
    temp: float
    target_temp: float
    device_name: str
    device_model_id: int
    device_sn: str
