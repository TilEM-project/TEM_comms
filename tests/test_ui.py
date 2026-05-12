from TEM_comms.ui import Run, Setup
from pydantic import ValidationError
import pytest


def test_run():
    Run(start=True)
    msg = Run()
    assert not msg.start


def test_run_retry_field():

    msg = Run()
    assert msg.retry is False

    msg = Run(retry=True)
    assert msg.retry is True
    assert msg.resume is False


def test_setup_defaults_all_false():
    msg = Setup()
    assert msg.auto_focus is False
    assert msg.lens_correction is False
    assert msg.survey is False


def test_setup_survey_flag():
    msg = Setup(survey=True)
    assert msg.survey is True
