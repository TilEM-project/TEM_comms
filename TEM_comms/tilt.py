from pigeon import BaseMessage
from typing import Optional
from pydantic import Field


class TiltMetadata(BaseMessage):
    """
    Shared tilt series metadata fields inherited by any message that
    reports per-acquisition tilt state.
    """

    tilt_angle: Optional[float] = Field(
        default=None,
        description="The tilt angle in degrees at which this acquisition was performed.",
    )
    tilt_series_id: Optional[str] = Field(
        default=None,
        description="The identifier grouping acquisitions in the same tilt series.",
        examples=["ts_a1b2c3d4e5f6"],
    )
    tilt_index: Optional[int] = Field(
        default=None,
        description="The 0-based position of this acquisition in the tilt series.",
    )
    tilt_total: Optional[int] = Field(
        default=None,
        description="The total number of tilt angles in the series.",
    )
