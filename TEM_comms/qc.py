from pigeon import BaseMessage
from typing import Literal, Optional
from pydantic import Field


class Status(BaseMessage):
    """
    This message contains the overall QC status of the system.
    """

    status: Literal["GOOD", "STOP_AT_END", "STOP_NOW"] = Field(
        description='The QC status, "GOOD" if imaging should continue, "STOP_AT_END" if imaging should be stopped at the end of the current montage, and "STOP_NOW" if imaging should be stopped immediately.'
    )
    reason: Optional[str] = Field(
        default=None,
        description="Optionally, a human readable reason for the current status.",
    )
