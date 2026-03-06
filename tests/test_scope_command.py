from TEM_comms.scope import Command
from pydantic import ValidationError
import pytest


def test_mag():
    with pytest.raises(ValidationError):
        Command(mag_mode="MAG")

    with pytest.raises(ValidationError):
        Command(mag=10)

    Command()
    Command(mag_mode="MAG", mag=1)


def test_mag_mode():
    with pytest.raises(ValidationError):
        Command(mag_mode="test", mag=1)

    with pytest.raises(ValidationError):
        Command(mag_mode="LM", mag=1)

    Command(mag_mode="MAG", mag=1)
    Command(mag_mode="LOWMAG", mag=1)
