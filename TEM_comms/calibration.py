from pigeon import BaseMessage
from typing import Mapping


class _Resolution(BaseMessage):
    nm_per_px: tuple[float, float]
    rotation: float


class Resolution(BaseMessage):
    lowmag: Mapping[int, _Resolution]
    mag: Mapping[int, _Resolution]


class Centroid(BaseMessage):
    aperture_id: int
    x: int
    y: int
