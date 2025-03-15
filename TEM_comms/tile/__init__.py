from .metadata import TileMetadata
from . import statistics


class Preview(TileMetadata):
    image: str


class Mini(TileMetadata):
    image: str


class Raw(TileMetadata):
    path: str


class Transform(TileMetadata):
    rotation: float
    x: float
    y: float


class Processed(TileMetadata):
    path: str
