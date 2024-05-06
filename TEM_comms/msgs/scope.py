from .base import BaseMessage

class Command(BaseMessage):
    focus: int | None = None
    aperture: int | None = None
    mag: int | None = None

class Status(BaseMessage):
    focus: int
    aperture: int
    mag: int
    vacuum: float
    tank_voltage: int