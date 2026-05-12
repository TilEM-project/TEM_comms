import pytest
from TEM_comms.acquisition_type import AcquisitionType


def test_enum_values():
    assert AcquisitionType.MONTAGE == "montage"
    assert AcquisitionType.TILT_SERIES == "tilt_series"
    assert AcquisitionType.LENS_CORRECTION == "lens_correction"
    assert AcquisitionType.SURVEY == "survey"


def test_enum_is_str_subclass():
    """str subclassing keeps wire compatibility."""
    assert isinstance(AcquisitionType.MONTAGE, str)
    assert AcquisitionType.MONTAGE == "montage"


def test_enum_construction_from_string():
    assert AcquisitionType("montage") == AcquisitionType.MONTAGE
    assert AcquisitionType("survey") == AcquisitionType.SURVEY


def test_enum_unknown_value_raises():
    with pytest.raises(ValueError):
        AcquisitionType("not_a_real_type")
