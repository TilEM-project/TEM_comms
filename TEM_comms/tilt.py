from pigeon import BaseMessage
from typing import Optional
from pydantic import Field


class TiltMetadata(BaseMessage):
    """Shared tilt series metadata fields.

    Inherited by any message that reports per-acquisition tilt state.
    """

    tilt_angle: Optional[float] = Field(
        default=None,
        description="The tilt angle in degrees at which this acquisition was performed.",
    )
    tilt_series_id: Optional[str] = Field(
        default=None,
        description="Identifier grouping acquisitions in the same tilt series.",
    )
    tilt_index: Optional[int] = Field(
        default=None,
        description="0-based position of this acquisition in the tilt series.",
    )
    tilt_total: Optional[int] = Field(
        default=None,
        description="Total number of tilt angles in the series.",
    )
