from pigeon import BaseMessage
from pydantic import Field
from typing import Optional


class TileMetadata(BaseMessage):
    tile_id: str = Field(
        description="The tile ID", examples=["69005602-15b0-4407-bf5b-4bddd6629141"]
    )
    montage_id: str = Field(
        description="The montage ID. If a zero length string, the tile is for UI display or calibration purposes only.",
        examples=["4330c7cf-e45b-4950-89cf-82dc0f815fe9"],
    )
    row: int = Field(
        description="The row of the montage where the tile was captured.", examples=[5]
    )
    column: int = Field(
        description="The column of the montage where the tile was captured.",
        examples=[24],
    )
    overlap: int = Field(
        description="The number of pixels of overlap between tiles.", examples=[512]
    )


class ProcessingOptions(BaseMessage):
    brightfield: Optional[bool] = Field(
        default=False,
        description="If true, this tile should be used in creating the brightfield image.",
    )
    darkfield: Optional[bool] = Field(
        default=False,
        description="If true, this tile should be used in creating the darkfield image.",
    )
    lens_correction: Optional[bool] = Field(
        default=False,
        description="If true, this tile is part of a lens correction montage.",
    )
