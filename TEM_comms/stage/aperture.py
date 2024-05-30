from pigeon import BaseMessage

class Command(BaseMessage):
    aperture_id: int | None = None
    calibrate: bool = False

class Status(BaseMessage):
    current_aperture: int
    calibrated: bool
    error: str = ""