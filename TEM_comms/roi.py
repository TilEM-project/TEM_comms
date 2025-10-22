from pigeon import BaseMessage
from typing import List, Tuple, Optional
from pydantic import Field


class Vertex(BaseMessage):
    x: float
    y: float


class ROI(BaseMessage):
    """
    Information about the current ROI being imaged.
    """

    vertices: List[Vertex] = Field(
        description="A list of points defining a polygonal ROI."
    )
    rotation_angle: float = Field(
        description="The rotation angle of the ROI in radians."
    )
    buffer_size: float = Field(
        default=0.0,
        description="The amount to dialate the ROI in nanometers when imaging.",
    )
    montage_id: str = Field(description="The montage ID to use when imaging the ROI.")
    specimen_id: Optional[str] = Field(
        default=None, description="The specimen ID corresponding to this ROI."
    )
    grid_id: Optional[str] = Field(
        default=None, description="The grid ID where this ROI should be imaged."
    )
    section_id: Optional[str] = Field(
        default=None, description="The section ID corresponding to this ROI."
    )
    metadata: Optional[dict] = Field(
        default=None, description="Extra metadata about this ROI."
    )
    queue_position: Optional[int] = Field(
        None, description="Position in queue, None means set as current"
    )


class LoadROI(BaseMessage):
    """
    This message can be used to load an ROI from the database into the ROI queue.
    """

    specimen_id: str = Field(description="The specimen ID to load from the database.")
    section_id: str = Field(description="The section ID to load from the database.")
    grid_id: Optional[str] = Field(
        default=None, description="The the grid ID where the section is loaded."
    )
    queue_position: Optional[int] = Field(
        None, description="Position in queue, None means set as current"
    )


class CreateROI(ROI):
    """
    This message can be used to create an ROI and add it to the ROI queue.
    """

    center: Optional[Vertex] = Field(
        default=None, description="The center point of the ROI."
    )
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
    """
    This message contains information on the status of an individual ROI.
    """

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
