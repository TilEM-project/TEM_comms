from typing import Optional

from pigeon import BaseMessage
from pydantic import Field

from .roi import Vertex


class Transform(BaseMessage):
    """This message contains the results of a lens correction solve, including the transform and residuals."""

    montage_id: str = Field(description="The lens-correction montage that was solved.")
    ok: bool = Field(
        default=True,
        description="True if the solve succeeded and artifacts were written.",
    )
    transform: str = Field(
        description="The base64-encoded lens correction transform (serialized mesh)."
    )
    residual_mean_px: float = Field(
        default=0.0, description="Mean solve residual in pixels."
    )
    residual_std_px: float = Field(
        default=0.0, description="Std of the solve residual in pixels."
    )
    n_matches: int = Field(
        default=0, description="Number of correspondences used in the solve."
    )


class LensCorrectionSetup(BaseMessage):
    """This message contains the parameters for a lens correction acquisition run."""

    enabled: bool = Field(
        default=False,
        description="Whether LC cadence is active during the next acquisition run.",
    )
    center: Vertex = Field(description="Stage nm coordinates for the LC region center.")
    tiles_x: Optional[int] = Field(
        default=None, ge=1, description="Tile grid columns. None = use service default."
    )
    tiles_y: Optional[int] = Field(
        default=None, ge=1, description="Tile grid rows. None = use service default."
    )
    overlap_pct: Optional[float] = Field(
        default=None,
        ge=0,
        le=100,
        description="Tile overlap percentage. None = use service default.",
    )
    every_n_rois: int = Field(
        default=0, ge=0, description="Fire LC every N ROIs. 0 = disabled."
    )
    every_n_tilt_steps: int = Field(
        default=0, ge=0, description="Fire LC every N tilt-series steps. 0 = disabled."
    )
