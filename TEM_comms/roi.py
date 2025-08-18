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


class CreateROI(ROI):
    center: Optional[Vertex] = None
    tilt_angles: Optional[List[float]] = Field(
        default=[0.0],
        description="List of tilt angles in degrees for tomography series",
    )
    aperture_centroid_pixel: Optional[Vertex] = Field(
        None, description="Aperture centroid in pixel coordinates"
    )
    aperture_centroid_physical: Optional[Vertex] = Field(
        None, description="Aperture centroid in physical coordinates (nm)"
    )
    overview_nm_per_pixel: Optional[float] = Field(
        None, description="Overview image scale in nm per pixel"
    )


class ROIStatus(BaseMessage):
    type: str = Field(
        description="Event type: roi_added, roi_advanced, queue_cleared, queue_empty"
    )
    timestamp: int = Field(description="Timestamp")
    roi_count: int = Field(description="Total number of active ROIs (queue + current)")
    has_active_rois: bool = Field(description="Whether there are any ROIs available")
    source: Optional[str] = Field(
        None, description="Source of last ROI submission: UI or external"
    )
    montage_id: Optional[str] = Field(None, description="Current montage ID")
    queue_info: Optional[dict] = Field(
        None, description="Queue statistics: total, completed, remaining"
    )
