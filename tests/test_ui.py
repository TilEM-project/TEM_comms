from TEM_comms.ui import Run, Setup
from pydantic import ValidationError
import pytest


def test_run():
    with pytest.raises(ValidationError):
        Run(montage=True, session_id="test", grid_first=1)

    with pytest.raises(ValidationError):
        Run(montage=True, session_id="test", grid_last=2)

    with pytest.raises(ValidationError):
        Run(montage=True, grid_first=1, grid_last=2)

    Run(montage=True, session_id="test", grid_first=1, grid_last=2)
    msg = Run()
    assert not msg.montage


def test_setup():
    with pytest.raises(ValidationError):
        Setup(mag_mode="LM")

    with pytest.raises(ValidationError):
        Setup(mag=10)

    Setup()
    Setup(mag_mode="LM", mag=1)
