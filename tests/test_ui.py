from TEM_comms.ui import Run, Setup
from pydantic import ValidationError
import pytest


def test_run():
    Run(montage=True)
    msg = Run()
    assert not msg.montage


def test_setup():
    with pytest.raises(ValidationError):
        Setup(mag_mode="LOWMAG")

    with pytest.raises(ValidationError):
        Setup(mag=10)

    Setup()
    Setup(mag_mode="LOWMAG", mag=1)
    Setup(mag_mode="MAG", mag=1)
