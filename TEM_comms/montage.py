from pigeon import BaseMessage
from typing import Mapping, List, Any


class Start(BaseMessage):
    montage_id: str
    num_tiles: int


class Finished(BaseMessage):
    montage_id: str
    num_tiles: int
    roi: str
    specimen: str
    metadata: Mapping[str, Any] | List[Any]
