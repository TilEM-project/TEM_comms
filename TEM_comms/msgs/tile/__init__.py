from ..base import BaseMessage
from . import statistics

class jpeg(BaseMessage):
    tile_id: str
    path: str

class minimap(BaseMessage):
    tile_id: str
    path: str

class processed(BaseMessage):
    tile_id: str
    path: str

class raw(BaseMessage):
    tile_id: str
    montage_id: str
    path: str
    row: int
    column: int
    overlap: float

class transform(BaseMessage):
    tile_id: str
    rotation: float
    x: float
    y: float