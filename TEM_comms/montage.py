from enum import StrEnum

from pigeon import BaseMessage
from typing import Mapping, Dict, Any, Optional, Tuple
from datetime import datetime
from pydantic import Field
from .tilt import TiltMetadata


class MontageState(StrEnum):
    """Lifecycle states for montage acquisition."""

    STARTED = "started"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    RESUMED = "resumed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    ERROR = "error"


class Status(TiltMetadata):
    """Published per-tile and on lifecycle transitions during montage acquisition."""

    montage_id: str = Field(description="The unique montage ID.")
    state: MontageState = Field(description="Current montage lifecycle state.")

    current_tile: int = Field(
        default=0, description="1-based tile index, 0 before first tile."
    )
    total_tiles: int = Field(
        default=0, description="Total planned tiles in this montage."
    )

    duration_seconds: Optional[float] = Field(
        default=None, description="Elapsed seconds since montage start."
    )
    avg_cycle_time_ms: Optional[float] = Field(
        default=None, description="Mean cycle time of last 10 tiles in ms."
    )
    stage_move_time_ms: Optional[float] = Field(
        default=None, description="Last tile's stage move time in ms."
    )
    capture_time_ms: Optional[float] = Field(
        default=None, description="Last tile's image capture time in ms."
    )
    throughput_tiles_per_min: Optional[float] = Field(
        default=None, description="Current throughput in tiles per minute."
    )
    estimated_completion: Optional[datetime] = Field(
        default=None, description="Estimated completion time (UTC)."
    )

    current_position: Optional[Tuple[int, int]] = Field(
        default=None, description="Current stage position [x, y] in nm."
    )
    error_message: Optional[str] = Field(
        default=None, description="Error description when state is ERROR."
    )


class Tile(BaseMessage):
    raster_index: int = Field(
        description="The index of the tile incremented for each subsequent tile in the montage."
    )
    stage_position: Tuple[int, int] = Field(
        description="The X-Y stage position of the tile in nanometers."
    )
    raster_position: Tuple[int, int] = Field(
        description="The X-Y indices of the tile in the montage."
    )


class Complete(TiltMetadata):
    """
    This message is sent after a montage is completed.
    """

    montage_id: str = Field(description="The unique montage ID.")
    tiles: Dict[str, Tile] = Field(
        description="A mapping from tile IDs to tile metadata."
    )
    acquisition_id: str = Field(description="The corresponding TEMdb acquisition ID.")
    start_time: datetime = Field(
        description="The timestamp when the montage was started."
    )
    pixel_size: float = Field(description="The average size ofee")
    rotation_angle: float = Field(
        description="The necessary tile rotation in radians to line up the right-handed image coordinate system with the Stage x-y coordinate system."
    )
    aperture_centroid: Tuple[int, int] = Field(
        description="The X-Y coordinates of the centroid of the imaged aperture in nanometers."
    )


class Minimap(BaseMessage):
    image: Optional[str] = Field(description="The map as a base 64 encoded image.")
    colorbar: str = Field(description="The colorbar as a base 64 encoded image.")
    min: Optional[float] = Field(description="The minimum value of the colorbar.")
    max: Optional[float] = Field(description="The maximum value of the colorbar.")


class Minimaps(BaseMessage):
    """
    This message contains multiple overview maps including a low resolution version of the montage, along with various statistics.
    """

    montage_id: str = Field(description="The unique montage ID.")
    montage: Minimap = Field(description="The montage minimap.")
    focus: Minimap = Field(description="The focus score map.")
