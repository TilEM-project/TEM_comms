from ..base import BaseMessage

class command(BaseMessage):
    aperture_id: int | None = None
    calibrate: bool = False

class status(BaseMessage):
    current_aperture: int
    calibrated: bool
    error: str = ""