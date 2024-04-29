from .base import BaseMessage

class command(BaseMessage):
    tile_id: str

class image(BaseMessage):
    tile_id: str
    path: str

class settings(BaseMessage):
    exposure: float | None = None
    width: int | None = None
    height: int | None = None

class status(BaseMessage):
    exposure: float
    width: int
    height: int
    temp: float
    target_temp: float
    device_name: str
    device_model_id: int
    sensor_model_id: int
    device_sn: str
    sensor_sn: str