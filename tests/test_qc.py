from TEM_comms.qc import Status, Tile, DetectedFault
from pydantic import ValidationError
import pytest


def test_bad_status():
    with pytest.raises(ValidationError):
        Status(state="BAD")


def test_tile_verdict_minimal():
    v = Tile(
        tile_id="t1", montage_id="m1", row=0, column=0, overlap=512, passed=True
    )
    assert v.passed is True
    assert v.faults == []


def test_tile_verdict_with_fault():
    f = DetectedFault(
        fault_type="beam_drift",
        severity=0.4,
        confidence=0.9,
        scope="persistent",
        metrics={"drift": 0.4},
    )
    v = Tile(
        tile_id="t1", montage_id="m1", row=2, column=3, overlap=512,
        passed=False, faults=[f],
    )
    assert v.passed is False
    assert len(v.faults) == 1
    assert v.faults[0].scope == "persistent"


def test_detected_fault_bad_scope():
    with pytest.raises(ValidationError):
        DetectedFault(
            fault_type="x", severity=0.1, confidence=0.1, scope="nope"
        )
