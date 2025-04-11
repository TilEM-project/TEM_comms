from pigeon import BaseMessage
from typing import Mapping, Dict, Any, Optional, Tuple
from datetime import datetime


class Tile(BaseMessage):
    raster_index: int
    stage_position: Tuple[int, int]
    raster_position: Tuple[int, int]


class Complete(BaseMessage):
    montage_id: str
    tiles: Dict[str, Tile]
    acquisition_id: str
    start_time: datetime
    pixel_size: float
    rotation_angle: float
    aperture_centroid: Tuple[int, int]


class Minimap(BaseMessage):
    image: Optional[str]
    colorbar: str
    min: Optional[float]
    max: Optional[float]


class Minimaps(BaseMessage):
    montage_id: str
    montage: Minimap
    focus: Minimap
