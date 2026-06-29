from pydantic import Field

from pigeon import BaseMessage

from .calibration_ops import CalibrationOptions


class Run(BaseMessage):
    """
    This message is used to control the start, stop, and pause of the acquisition of ROIs. It also contains some fields for retrying or canceling an acquisition in the event of a failure.
    """

    start: bool = Field(
        default=False,
        description="Begin acquiring ROIs according to the ROI queue.",
    )
    abort_now: bool = Field(default=False, description="Stop imaging immediately.")
    abort_at_end: bool = Field(
        default=False, description="Stop imaging after the current montage is complete."
    )
    pause: bool = Field(
        default=False,
        description="Pause imaging during the current montage, then resume when ready.",
    )
    resume: bool = Field(
        default=False,
        description="Resume a paused montage. For retrying after a failure, use the retry field.",
    )
    retry: bool = Field(
        default=False,
        description="Retry the current state machine from a failure state.",
    )
    cancel: bool = Field(
        default=False, description="Return to preview mode from a failure state."
    )


class Setup(CalibrationOptions):
    """This message is utilized to setup a microscope in a semi-automated manner. Each of the fields in this message instructs the system to run an individual setup routine."""

    survey: bool = Field(
        default=False,
        description="Trigger a low-magnification survey acquisition with bootstrap-built ROI.",
    )
