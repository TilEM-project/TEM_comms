from pigeon import BaseMessage
from pydantic import Field


class Command(BaseMessage):
    """This message is used to trigger a choreographed sample transfer between stations."""

    station: str | None = Field(
        default=None,
        description="The target station name (e.g., 'microscope', 'loadlock', 'exchange'), or None for no action.",
    )


class Status(BaseMessage):
    """This message contains the status of the sample transfer system."""

    current_station: str = Field(
        description="The name of the current station, or 'unknown' if not calibrated, or 'in_transit' during a transfer.",
    )
    target_station: str | None = Field(
        default=None,
        description="The target station name during a transfer, or None if idle.",
    )
    in_transit: bool = Field(
        default=False,
        description="True if a transfer is currently in progress.",
    )
    step: int = Field(
        default=0,
        description="The current step number in the transfer sequence (0 if idle).",
    )
    total_steps: int = Field(
        default=0,
        description="The total number of steps in the current transfer sequence (0 if idle).",
    )
    error: str = Field(
        default="",
        description="An optional error message.",
    )
