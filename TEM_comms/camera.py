from pigeon import BaseMessage
from .tile.metadata import TileMetadata
from typing import Optional


class Command(TileMetadata):
    brightfield: Optional[bool] = False
    darkfield: Optional[bool] = False
    lens_correction: Optional[bool] = True


class Image(BaseMessage):
    tile_id: str
    montage_id: str


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
    bit_depth: int | str
