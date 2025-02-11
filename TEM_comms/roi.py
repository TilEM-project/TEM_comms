from pigeon import BaseMessage
from typing import List, Tuple, Optional
from pydantic import Field


class Vertex(BaseMessage):
    x: float
    y: float


class ROI(BaseMessage):
    vertices: List[Vertex]
    rotation_angle: float
    buffer_size: float = 0.0
    montage_id: str
    specimen_id: Optional[str] = None
    grid_id: Optional[str] = None
    section_id: Optional[str] = None
    metadata: Optional[dict] = None
    queue_position: Optional[int] = Field(
        None, description="Position in queue, None means set as current"
    )


class LoadROI(BaseMessage):
    specimen_id: str
    section_id: str
    grid_id: Optional[str] = None
    queue_position: Optional[int] = Field(
        None, description="Position in queue, None means set as current"
    )


class CreateROI(BaseMessage):
    center: Vertex
    width: float
    height: float
    rotation_angle: float = 0.0
    montage_id: str
    specimen_id: Optional[str] = None
    grid_id: Optional[str] = None
    section_id: Optional[str] = None
    queue_position: Optional[int] = Field(
        None, description="Position in queue, None means set as current"
    )
