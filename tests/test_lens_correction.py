import pytest
from TEM_comms.lens_correction import LensCorrectionSetup, Transform
from TEM_comms.roi import Vertex

from TEM_comms import topics


def test_setup_defaults():
    msg = LensCorrectionSetup(center=Vertex(x=0, y=0))
    assert msg.enabled is False
    assert msg.tiles_x == 10
    assert msg.tiles_y == 10
    assert msg.overlap_pct == 60.0
    assert msg.every_n_rois == 0
    assert msg.every_n_tilt_steps == 0


def test_setup_explicit_values():
    msg = LensCorrectionSetup(
        enabled=True,
        center=Vertex(x=12345.0, y=-6789.0),
        tiles_x=8,
        tiles_y=12,
        overlap_pct=50,
        every_n_rois=3,
        every_n_tilt_steps=5,
    )
    assert msg.enabled is True
    assert msg.center.x == 12345.0
    assert msg.tiles_x == 8
    assert msg.every_n_rois == 3


def test_setup_validates_negatives():
    with pytest.raises(Exception):
        LensCorrectionSetup(center=Vertex(x=0, y=0), tiles_x=0)
    with pytest.raises(Exception):
        LensCorrectionSetup(center=Vertex(x=0, y=0), every_n_rois=-1)
    with pytest.raises(Exception):
        LensCorrectionSetup(center=Vertex(x=0, y=0), overlap_pct=120)


def test_topic_registered():
    assert topics["lens_correction.setup"] is LensCorrectionSetup


def test_transform_unchanged():
    msg = Transform(transform="abc")
    assert msg.transform == "abc"


def test_setup_roundtrip():
    msg = LensCorrectionSetup(
        center=Vertex(x=1.0, y=2.0),
        enabled=True,
        tiles_x=8,
        tiles_y=12,
        overlap_pct=55.5,
        every_n_rois=2,
        every_n_tilt_steps=4,
    )
    assert LensCorrectionSetup.deserialize(msg.serialize()) == msg
