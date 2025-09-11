from pigeon import BaseMessage
from typing import Optional, List, Tuple, Mapping
from pydantic import model_validator, Field


class Calibrate(BaseMessage):
    """
    This message is used to calibrate the image shifting system.
    """

    position: int = Field(description="The image shift position index to calibrate.")
    image_shift: Tuple[int, int] = Field(
        description="The new calibration values for this position index."
    )


class Status(BaseMessage):
    """
    This message conatins the status of the image shifting system.
    """

    enabled: bool = Field(
        description="If the image shifting system is currently enabled."
    )
    current_position: int | None = Field(
        default=None, description="The current position index, or None if disabled."
    )
    image_shift: Tuple[int, int] = Field(
        description="The current image shift calibration values."
    )
    calibration: Mapping[int, Tuple[int, int]] = Field(
        description="The calibration values for each position index."
    )

    @model_validator(mode="after")
    def check_current_position(self):
        assert self.enabled == (self.current_position is not None)
        return self


class Command(BaseMessage):
    """
    This message is used to enable and disable the image shifting system, and to switch to a predefined position.
    """

    enable: bool = Field(
        description="Used to enable and disable the image shifting system."
    )
    position: Optional[int] = Field(
        default=None,
        description="The calibrated position index to use, or None if disabled.",
    )

    @model_validator(mode="after")
    def check_position(self):
        assert self.enable == (self.position is not None)
        return self
