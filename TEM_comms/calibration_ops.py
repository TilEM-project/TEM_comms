from pigeon import BaseMessage
from pydantic import Field


class CalibrationOptions(BaseMessage):
    """Modality-agnostic calibration operations.

    All defaults False — the requester opts in to each op explicitly.
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
    bright_field: bool = Field(
        default=False, description="Acquire a brightfield image."
    )
    dark_field: bool = Field(
        default=False, description="Acquire a darkfield image."
    )
    beam_center: bool = Field(
        default=False, description="Center the beam in the image frame."
    )
    beam_spread: bool = Field(
        default=False, description="Spread the beam."
    )
    find_aperture: bool = Field(
        default=False, description="Find and move to the aperture centroid."
    )
    calibrate_resolution: bool = Field(
        default=False,
        description="Calibrate the resolution of the microscope at the current mag level.",
    )


class TiltCalibrationOptions(BaseMessage):

    eucentric_height: bool = Field(
        default=True,
        description="Recover eucentric height after tilting (Z-axis correction).",
    )
    track_feature: bool = Field(
        default=True,
        description="Track a fiducial / feature across tilt steps to keep ROI centered.",
    )
    beam_tilt_compensation: bool = Field(
        default=True,
        description="Apply beam-tilt compensation to keep illumination on-axis.",
    )
