from pigeon import BaseMessage
from typing import Optional, Literal
from pydantic import model_validator, Field


class Edit(BaseMessage):
    """
    This message is used to edit existing ROIs in the ROI queue.
    """

    roi_id: str = Field(description="The ROI id to edit.")
    roi_pos_x: int = Field(description="The new X position of the ROI in nanometers.")
    roi_pox_y: int = Field(description="The new Y position of the ROI in nanometers.")
    roi_width: int = Field(description="The new width of the ROI in nanometers.")
    roi_height: int = Field(description="The new height of the ROI in nanometers.")
    roi_angle: float = Field(description="The new angle to rotate the ROI in radians.")


class Run(BaseMessage):
    """
    This message is used start and stop automated image acquisition.
    """

    montage: bool = Field(
        default=False,
        description="Begin collecting montages according to the ROI queue.",
    )
    abort_now: bool = Field(default=False, description="Stop imaging immediately.")
    abort_at_end: bool = Field(
        default=False, description="Stop imaging after the current montage is complete."
    )
    resume: bool = Field(default=False, description="Resume from a failure state.")
    cancel: bool = Field(
        default=False, description="Return to preview mode from a failure state."
    )


class Setup(BaseMessage):
    """
    This message is utilized to setup a microscope in a semi-automated manner. Each of the fields in this message instructs the system to run an individual setup routine.
    """

    auto_focus: bool = Field(
        default=False, description="Automatically focus the microscope."
    )
    auto_exposure: bool = Field(
        default=False, description="Optimize the camera exposure."
    )
    lens_correction: bool = Field(
        default=False, description="Collect and generate a lens correction."
    )
    acquire_brightfield: bool = Field(
        default=False, description="Acquire a darkfield image."
    )
    acquire_darkfield: bool = Field(
        default=False, description="Acquire a brightfield image."
    )
    center_beam: bool = Field(
        default=False, description="Center the beam in the image frame."
    )
    spread_beam: bool = Field(default=False, description="Spread the beam.")
    find_aperture: bool = Field(
        default=False, description="Find and move to the aperture centroid."
    )
    calibrate_resolution: bool = Field(
        default=False,
        description="Calibrate the resolution of the microscope at the current mag level.",
    )
    grid: Optional[int] = Field(
        default=None, description="Change to the specified grid."
    )
    mag_mode: Optional[Literal["LM", "MAG1", "MAG2"]] = Field(
        default=None,
        description='Change to the specified mag mode. The "mag" field must also be specified.',
    )
    mag: Optional[int] = Field(
        default=None,
        description='Change to the specified magnification. "mga_mode" must also be specified.',
    )

    @model_validator(mode="after")
    def check_mag(self):
        assert (self.mag_mode is None) == (self.mag is None)
        return self
