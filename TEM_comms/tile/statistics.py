from pigeon import BaseMessage

class Focus(BaseMessage):
    tile_id: str
    focus: float

class Histogram(BaseMessage):
    tile_id: str
    path: str

class MinMaxMean(BaseMessage):
    tile_id: str
    min: int
    max: int
    mean: int