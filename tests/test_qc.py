from TEM_comms.qc import Status
from pydantic import ValidationError
import pytest


def test_bad_status():
    with pytest.raises(ValidationError):
        Status(state="BAD")
