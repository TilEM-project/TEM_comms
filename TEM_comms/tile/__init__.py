from .metadata import TileMetadata
from . import statistics
from pydantic import BaseModel, Field
from typing import Literal, List


class Preview(TileMetadata):
    """
    This message contains a downsampled tile image used for UI and calibration purposes.
    """

    image: str = Field(description="The downsampled tile as a base 64 encoded string.")


class Mini(TileMetadata):
    """
    This message contains a highly downsampled tile image used in the creation of a minimap.
    """

    image: str = Field(description="The downsampled tile as a base 64 encoded string.")


class Raw(TileMetadata):
    """
    This message is sent whenever a new tile is stored on the filesystem and is ready for processing.
    """

    path: str = Field(
        description="The path where the raw tile is stored.",
        examples=["/storage/raw/69005602-15b0-4407-bf5b-4bddd6629141.tiff"],
    )


class Match(BaseModel):
    model_config = {"extra": "forbid"}
    row: int = Field(description="The row of the neighboring tile.")
    column: int = Field(description="The column of the neighboring tile.")
    dX: float = Field(
        description="The X axis offset of the tile in pixels to get the tile to match."
    )
    dY: float = Field(
        description="The Y axis offset of the tile in pixels to get the tile to match."
    )
    dXsd: float = Field(
        description="The X axis offset standard deviation of all the feature matches."
    )
    dYsd: float = Field(
        description="The Y axis offset standard deviation of all the feature matches."
    )
    distance: float = Field(description="The euclidian offset distance in pixels.")
    rotation: float = Field(
        description="The tile rotation in radians necessary to get the tiles to match."
    )
    match_quality: float = Field(description="A metric for the quality of the match.")
    position: Literal["top", "bottom", "left", "right"] = Field(
        description="The position of matched tile relative to the captured tile."
    )
    pX: List[int] = Field(description="The captured tile feature X positions.")
    pY: List[int] = Field(description="The captured tile feature Y positions.")
    qX: List[int] = Field(description="The matched tile feature X positions.")
    qY: List[int] = Field(description="The matched tile feature Y positions.")


class Matches(TileMetadata):
    """
    This message contains data relating to the matching of neighboring tiles.
    """

    matches: List[Match] = Field(
        description="Information about how the captured tile matches to each of its available neighbors."
    )


class Processed(TileMetadata):
    """
    This message contains the path to a fully processed tile stored on the filesystem.
    """

    path: str = Field(
        description="The path where the processed tile is stored.",
        examples=["/storage/processed/69005602-15b0-4407-bf5b-4bddd6629141.tiff"],
    )
