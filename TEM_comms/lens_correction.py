from pigeon import BaseMessage
from pydantic import Field

from .roi import Vertex


class Transform(BaseMessage):
    """
    This message contains a compact representation of the generated lens correction transform.
    """

    transform: str = Field(description="The base64 encoded lens correction transform.")


class LensCorrectionSetup(BaseMessage):
    """This message contains the parameters for a lens correction acquisition run.
    """

    enabled: bool = Field(
        default=False,
        description="Whether LC cadence is active during the next acquisition run.",
    )
    center: Vertex = Field(
        description="Stage nm coordinates for the LC region center."
    )
    tiles_x: int = Field(
        default=10, ge=1, description="Tile grid columns."
    )
    tiles_y: int = Field(
        default=10, ge=1, description="Tile grid rows."
    )
    overlap_pct: float = Field(
        default=60.0, ge=0, le=100, description="Tile overlap percentage."
    )
    every_n_rois: int = Field(
        default=0, ge=0, description="Fire LC every N ROIs. 0 = disabled."
    )
    every_n_tilt_steps: int = Field(
        default=0, ge=0, description="Fire LC every N tilt-series steps. 0 = disabled."
    )
