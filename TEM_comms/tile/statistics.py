from .metadata import TileMetadata
from typing import List
from pydantic import Field


class Focus(TileMetadata):
    """
    This message contains the focus score, a measure of the quality of the focus of a given tile.
    """

    focus: float = Field(
        description="The focus metric. Lower is better", ge=0, le=1, examples=[0.37]
    )


class Histogram(TileMetadata):
    """
    This message contains raw histogram data for a tile.
    """

    hist: List[int] = Field(description="The raw histogram data.")


class MinMaxMean(TileMetadata):
    """
    This message contains simple statistics about a processed tile.
    """

    min: int = Field(description="The minimum pixel value.", examples=[5])
    max: int = Field(description="The maximum pixel value.", examples=[249])
    mean: int = Field(description="The mean pixel value.", examples=[187])
    std: int = Field(
        description="The standard deviation of the pixel values.", examples=[25]
    )
