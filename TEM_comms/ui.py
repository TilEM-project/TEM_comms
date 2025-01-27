from pigeon import BaseMessage
from typing import Optional, Literal
from pydantic import model_validator


class Edit(BaseMessage):
    roi_id: str
    roi_pos_x: int
    roi_pox_y: int
    roi_width: int
    roi_height: int
    roi_angle: float


class Run(BaseMessage):
    session_id: Optional[str] = None
    grid_first: Optional[int] = None
    grid_last: Optional[int] = None
    montage: bool = False
    abort_now: bool = False
    abort_at_end: bool = False
    resume: bool = False

    @model_validator(mode="after")
    def check_grid(self):
        assert self.montage != (self.grid_first is None)
        assert self.montage != (self.grid_last is None)
        return self

    @model_validator(mode="after")
    def check_session(self):
        assert self.montage != (self.session_id is None)
        return self


class Setup(BaseMessage):
    conch_owner: Optional[str] = None
    auto_focus: bool = False
    auto_exposure: bool = False
    lens_correction: bool = False
    acquire_brightfield: bool = False
    acquire_darkfield: bool = False
    center_beam: bool = False
    spread_beam: bool = False
    find_aperture: bool = False
    calibrate_resolution: bool = False
    grid: Optional[int] = None
    mag_mode: Optional[Literal["LM", "MAG1", "MAG2"]] = None
    mag: Optional[int] = None

    @model_validator(mode="after")
    def check_mag(self):
        assert (self.mag_mode is None) == (self.mag is None)
        return self
