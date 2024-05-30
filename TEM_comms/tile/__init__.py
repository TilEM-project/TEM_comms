from pigeon import BaseMessage
from . import statistics


class JPEG(BaseMessage):
    tile_id: str
    path: str


class Minimap(BaseMessage):
    tile_id: str
    path: str


class Processed(BaseMessage):
    tile_id: str
    path: str


class Raw(BaseMessage):
    tile_id: str
    montage_id: str
    path: str
    row: int
    column: int
    overlap: float


class Transform(BaseMessage):
    tile_id: str
    rotation: float
    x: float
    y: float
