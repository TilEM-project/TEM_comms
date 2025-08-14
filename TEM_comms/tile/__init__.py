from .metadata import TileMetadata
from . import statistics
from pydantic import BaseModel
from typing import Literal, List


class Preview(TileMetadata):
    image: str


class Mini(TileMetadata):
    image: str


class Raw(TileMetadata):
    path: str


class Match(BaseModel):
    model_config = {"extra": "forbid"}
    row: int
    column: int
    dX: float
    dY: float
    dXsd: float
    dYsd: float
    distance: float
    rotation: float
    match_quality: float
    position: Literal["top", "bottom", "left", "right"]
    pX: List[int]
    pY: List[int]
    qX: List[int]
    qY: List[int]


class Matches(TileMetadata):
    matches: List[Match]


class Processed(TileMetadata):
    path: str
