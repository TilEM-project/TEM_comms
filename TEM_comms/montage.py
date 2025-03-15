from pigeon import BaseMessage
from typing import Mapping, List, Any, Optional


class Start(BaseMessage):
    montage_id: str
    num_tiles: int


class Finished(BaseMessage):
    montage_id: str
    num_tiles: int
    roi: str
    specimen: str
    metadata: Mapping[str, Any] | List[Any]


class Minimap(BaseMessage):
    image: Optional[str]
    colorbar: str
    min: Optional[float]
    max: Optional[float]


class Minimaps(BaseMessage):
    montage_id: str
    montage: Minimap
    focus: Minimap
