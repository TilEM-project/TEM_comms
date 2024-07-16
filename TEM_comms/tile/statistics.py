from pigeon import BaseMessage


class Focus(BaseMessage):
    montage_id: str
    tile_id: str
    focus: float


class Histogram(BaseMessage):
    montage_id: str
    tile_id: str
    path: str


class MinMaxMean(BaseMessage):
    montage_id: str
    tile_id: str
    min: int
    max: int
    mean: int

