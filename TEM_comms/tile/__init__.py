from pigeon import BaseMessage
from . import statistics


class Preview(BaseMessage):
    tile_id: str
    image: str


class Minimap(BaseMessage):
    tile_id: str
    path: str


class Raw(BaseMessage):
    tile_id: str
    montage_id: str
    path: str
    row: int
    column: int
    overlap: int


class Transform(BaseMessage):
    montage_id: str
    tile_id: str
    rotation: float
    x: float
    y: float


class Processed(BaseMessage):
    montage_id: str
    tile_id: str
    path: str
