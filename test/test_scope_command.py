from TEM_comms.msgs.scope import command
from pydantic import ValidationError
import pytest

def test_mag():
    with pytest.raises(ValidationError):
        command(mag_mode="LM")
    
    with pytest.raises(ValidationError):
        command(mag=10)

    command()
    command(mag_mode="LM", mag=1)

def test_mag_mode():
    with pytest.raises(ValidationError):
        command(mag_mode="test", mag=1)

    command(mag_mode="LM", mag=1)
    command(mag_mode="MAG2", mag=1)
    command(mag_mode="MAG2", mag=1)