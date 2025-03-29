from pigeon import BaseMessage
from typing import Mapping, List, Any, Optional, Tuple
from datetime import datetime


class Complete(BaseMessage):
    montage_id: str
    tile_ids: List[str]
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
