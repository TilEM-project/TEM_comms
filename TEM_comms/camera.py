from pigeon import BaseMessage
from .tile.metadata import TileMetadata, ProcessingOptions
from typing import Optional
from pydantic import Field


class Command(TileMetadata, ProcessingOptions):
    """
    This message is used to instruct the camera to capture an image.
    """


class Image(BaseMessage):
    """
    This message is sent after the camera exposure is complete.
    """

    tile_id: str = Field(
        description="The tile ID", examples=["69005602-15b0-4407-bf5b-4bddd6629141"]
    )
    montage_id: str = Field(
        description="The montage ID. If a zero length string, the tile is for UI display or calibration purposes only.",
        examples=["4330c7cf-e45b-4950-89cf-82dc0f815fe9"],
    )


class Settings(BaseMessage):
    """
    This message is used to change camera settings.
    """

    exposure: float | None = Field(
        default=None, description="The length of the camera exposure in microseconds."
    )
    gain: Optional[float] = Field(
        default=None, description="The camera gain in decibels."
    )
    width: int | None = Field(
        default=None, description="The width of the camera frame."
    )
    height: int | None = Field(
        default=None, description="The height of the camera frame."
    )


class Status(BaseMessage):
    """
    This message contains information about the state of the camera.
    """

    exposure: float = Field(
        description="The length of the camera exposure in microseconds."
    )
    gain: float = Field(description="The camera gain in decibels.")
    width: int = Field(description="The camera frame width.")
    height: int = Field(description="The camera frame height.")
    temp: float = Field(description="The camera temperature.")
    target_temp: float = Field(
        description="The target temperature of the camera cooling system."
    )
    device_name: str = Field(description="The human readable device name.")
    device_model_id: str = Field(description="The device model identifier.")
    device_sn: str = Field(description="The camera serial number.")
    bit_depth: int | str = Field(description="The bit depth of the camera sensor.")
