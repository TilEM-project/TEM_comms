from TEM_comms.stage.motion import Command as MotionCommand, Status as MotionStatus
from TEM_comms.stage.aperture import (
    Command as ApertureCommand,
    Status as ApertureStatus,
)


def test_motion_command_with_extra_fields():
    command = MotionCommand(x=10, y=20, z=30, calibrate=True, wait_for_settle=True)
    assert command.x == 10
    assert command.y == 20
    assert command.z == 30
    assert command.calibrate is True
    assert command.wait_for_settle is True


def test_motion_status_with_extra_fields():
    status = MotionStatus(
        x=10, y=20, z=30, in_motion=True, error="", extra_field="extra_value"
    )
    assert status.x == 10
    assert status.y == 20
    assert status.z == 30
    assert status.in_motion is True
    assert status.error == ""
    assert status.extra_field == "extra_value"


def test_aperture_command_with_extra_fields():
    command = ApertureCommand(aperture_id=1, calibrate=True, extra_field="extra_value")
    assert command.aperture_id == 1
    assert command.calibrate is True
    assert command.extra_field == "extra_value"


def test_aperture_status_with_extra_fields():
    status = ApertureStatus(
        current_aperture=1, calibrated=True, error="", extra_field="extra_value"
    )
    assert status.current_aperture == 1
    assert status.calibrated is True
    assert status.error == ""
    assert status.extra_field == "extra_value"
