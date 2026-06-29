from enum import Enum


class AcquisitionType(str, Enum):
    MONTAGE = "montage"
    TILT_SERIES = "tilt_series"
    LENS_CORRECTION = "lens_correction"
    SURVEY = "survey"
