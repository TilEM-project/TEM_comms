from pigeon import BaseMessage
from typing import Mapping, Dict, Any, Optional, Tuple
from datetime import datetime
from pydantic import Field


class Tile(BaseMessage):
    raster_index: int = Field(
        description="The index of the tile incremented for each subsequent tile in the montage."
    )
    stage_position: Tuple[int, int] = Field(
        description="The X-Y stage position of the tile in nanometers."
    )
    raster_position: Tuple[int, int] = Field(
        description="The X-Y indicies of the tile in the montage."
    )


class Complete(BaseMessage):
    """
    This message is sent after a montage is completed.
    """

    montage_id: str = Field(description="The unique montage ID.")
    tiles: Dict[str, Tile] = Field(
        description="A mapping from tile IDs to tile metadata."
    )
    acquisition_id: str = Field(description="The corresponding TEMdb acqusition ID.")
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
