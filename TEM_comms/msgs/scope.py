from .base import BaseMessage

class command(BaseMessage):
    focus: int | None = None
    aperture: int | None = None
    mag: int | None = None

class status(BaseMessage):
    focus: int
    aperture: int
    mag: int
    vacuum: float
    tank_voltage: int