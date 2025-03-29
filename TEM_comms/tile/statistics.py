from .metadata import TileMetadata
from typing import List


class Focus(TileMetadata):
    focus: float


class Histogram(TileMetadata):
    hist: List[int]


class MinMaxMean(TileMetadata):
    min: int
    max: int
    mean: int
    std: int
