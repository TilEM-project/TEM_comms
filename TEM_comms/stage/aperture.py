from pigeon import BaseMessage
from pydantic import ConfigDict


class Command(BaseMessage):
    model_config = ConfigDict(extra="allow")

    aperture_id: int | None = None
    calibrate: bool = False


class Status(BaseMessage):
    model_config = ConfigDict(extra="allow")

    current_aperture: int | None
    calibrated: bool
    error: str = ""
