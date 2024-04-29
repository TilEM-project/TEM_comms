from ..base import BaseMessage

class focus(BaseMessage):
    tile_id: str
    focus: float

class histogram(BaseMessage):
    tile_id: str
    path: str

class min_max_mean(BaseMessage):
    tile_id: str
    min: int
    max: int
    mean: int