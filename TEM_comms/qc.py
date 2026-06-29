from pigeon import BaseMessage
from typing import Literal, Optional, List
from pydantic import BaseModel, Field

from .tile.metadata import TileMetadata


class Status(BaseMessage):
    """Overall (run-level) QC status of the system."""

    status: Literal["GOOD", "STOP_AT_END", "STOP_NOW"] = Field(
        description='The QC status, "GOOD" if imaging should continue, "STOP_AT_END" if imaging should be stopped at the end of the current montage, and "STOP_NOW" if imaging should be stopped immediately.'
    )
    reason: Optional[str] = Field(
        default=None,
        description="Optionally, a human readable reason for the current status.",
    )


class DetectedFault(BaseModel):
    """A single fault detected on a tile."""

    model_config = {"extra": "forbid"}

    fault_type: str = Field(description="Fault name, e.g. 'beam_drift'.")
    severity: float = Field(description="Estimated severity, 0..1.", ge=0, le=1)
    confidence: float = Field(description="Detector confidence, 0..1.", ge=0, le=1)
    scope: Literal["transient", "persistent", "critical"] = Field(
        description="transient = one tile; persistent = poisons later tiles; critical = damage/unrecoverable."
    )
    metrics: dict = Field(
        default={}, description="Raw features that triggered detection."
    )


class Tile(TileMetadata):
    """Per-tile QC verdict."""

    passed: bool = Field(description="True if the tile passed QC.")
    faults: List[DetectedFault] = Field(
        default=[], description="Faults detected on this tile."
    )
