from pigeon import BaseMessage
from typing import List, Tuple, Optional
from enum import Enum
from pydantic import Field
from .tilt import TiltMetadata


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
        description="The amount to dilate the ROI in nanometers when imaging.",
    )
    montage_id: str = Field(description="The montage ID to use when imaging the ROI.")
    specimen_id: Optional[str] = Field(
        default=None, description="The specimen ID corresponding to this ROI."
    )
    aperture_id: Optional[int] = Field(
        default=None,
        description="The aperture ID to navigate to before imaging this ROI.",
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
    aperture_id: Optional[int] = Field(
        default=None, description="The aperture ID where the section is loaded."
    )
    queue_position: Optional[int] = Field(
        None, description="Position in queue, None means set as current"
    )


class CreateROI(ROI):
    """
    This message is used to create an ROI and add it to the ROI queue.
    """

    center: Optional[Vertex] = Field(
        default=None, description="The center point of the ROI."
    )
    tilt_angles: Optional[List[float]] = Field(
        default=[0.0],
        description="The list of tilt angles in degrees for a tomography series.",
    )
    aperture_centroid_pixel: Optional[Vertex] = Field(
        None, description="The aperture centroid in pixel coordinates."
    )
    aperture_centroid_physical: Optional[Vertex] = Field(
        None, description="The aperture centroid in physical coordinates (nm)."
    )
    overview_nm_per_pixel: Optional[float] = Field(
        None, description="The overview image scale in nanometers per pixel."
    )
    roi_name: Optional[str] = Field(
        default=None, description="The human-readable ROI name for queue display."
    )


class ROIEntryStatus(str, Enum):
    """
    The lifecycle status of an ROI queue entry.
    """

    PENDING = "pending"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETE = "complete"
    FAILED = "failed"
    ABORTED = "aborted"


class ROIStatus(TiltMetadata):
    """
    This message contains the status of an individual ROI in the acquisition queue.
    """

    montage_id: str = Field(
        description="The montage ID for this ROI entry.",
        examples=["ROI-1_20260314T143025"],
    )
    roi_name: Optional[str] = Field(
        default=None, description="The human-readable ROI name from the UI."
    )
    status: ROIEntryStatus = Field(
        description="The lifecycle status of this ROI entry."
    )
    timestamp: int = Field(description="The Unix timestamp of the last status change.")
    source: Optional[str] = Field(
        default=None,
        description="The source of the ROI submission: UI or external.",
    )
    current_tile: Optional[int] = Field(
        default=None,
        description="The current tile index (1-based) when the ROI is active.",
    )
    total_tiles: Optional[int] = Field(
        default=None,
        description="The total number of planned tiles for this montage.",
    )
    error_message: Optional[str] = Field(
        default=None,
        description="The error description when status is failed.",
    )


class QueueStatus(BaseMessage):
    """
    This message contains a full snapshot of the acquisition queue.
    """

    queue: List[ROIStatus] = Field(
        description="The ordered list of all ROI entries in the queue.",
    )
    active_montage_id: Optional[str] = Field(
        default=None,
        description="The montage ID of the currently active or paused ROI.",
    )
    completed_count: int = Field(
        description="The number of ROIs that have completed successfully.",
    )
    timestamp: int = Field(description="The Unix timestamp of this snapshot.")


class QueueUpdate(BaseMessage):
    """
    This message is used to manipulate the acquisition queue during a paused state.
    """

    remove: Optional[List[str]] = Field(
        default=None,
        description="The list of montage IDs to remove from the pending queue.",
    )
    reorder: Optional[List[str]] = Field(
        default=None,
        description="The new queue order as an ordered list of montage IDs.",
    )
