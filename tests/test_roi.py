import pytest
from pydantic import ValidationError
from TEM_comms.acquisition_type import AcquisitionType
from TEM_comms.calibration_ops import CalibrationOptions, TiltCalibrationOptions
from TEM_comms.roi import (
    CreateROI,
    QueueStatus,
    QueueUpdate,
    ROIEntryStatus,
    ROIStatus,
    Vertex,
)

from TEM_comms import topics


def test_roi_entry_status_values():
    assert ROIEntryStatus.PENDING == "pending"
    assert ROIEntryStatus.ACTIVE == "active"
    assert ROIEntryStatus.PAUSED == "paused"
    assert ROIEntryStatus.COMPLETE == "complete"
    assert ROIEntryStatus.FAILED == "failed"
    assert ROIEntryStatus.ABORTED == "aborted"


def test_roi_entry_status_from_string():
    assert ROIEntryStatus("pending") == ROIEntryStatus.PENDING


def test_roi_entry_status_invalid():
    with pytest.raises(ValueError):
        ROIEntryStatus("invalid")


def test_roi_status():
    status = ROIStatus(
        montage_id="ROI-1_20260314T143025",
        status=ROIEntryStatus.PENDING,
        timestamp=1000,
    )
    assert status.montage_id == "ROI-1_20260314T143025"
    assert status.status == ROIEntryStatus.PENDING
    assert status.roi_name is None
    assert status.current_tile is None
    assert status.total_tiles is None
    assert status.error_message is None
    assert status.tilt_angle is None
    assert status.tilt_series_id is None


def test_roi_status_with_tilt_and_progress():
    status = ROIStatus(
        montage_id="ROI-1_tilt00",
        roi_name="ROI-1",
        status=ROIEntryStatus.ACTIVE,
        timestamp=1000,
        current_tile=5,
        total_tiles=100,
        tilt_angle=0.0,
        tilt_series_id="ts_abc123def456",
        tilt_index=0,
        tilt_total=3,
    )
    assert status.current_tile == 5
    assert status.total_tiles == 100
    assert status.tilt_index == 0


def test_roi_status_failed():
    status = ROIStatus(
        montage_id="test",
        status=ROIEntryStatus.FAILED,
        timestamp=1000,
        error_message="Stage move timeout",
    )
    assert status.error_message == "Stage move timeout"


def test_queue_status_empty():
    qs = QueueStatus(queue=[], completed_count=0, timestamp=1000)
    assert len(qs.queue) == 0
    assert qs.active_montage_id is None


def test_queue_status_with_entries():
    qs = QueueStatus(
        queue=[
            ROIStatus(montage_id="roi1", status=ROIEntryStatus.COMPLETE, timestamp=100),
            ROIStatus(
                montage_id="roi2",
                status=ROIEntryStatus.ACTIVE,
                timestamp=200,
                current_tile=5,
                total_tiles=50,
            ),
            ROIStatus(montage_id="roi3", status=ROIEntryStatus.PENDING, timestamp=200),
        ],
        active_montage_id="roi2",
        completed_count=1,
        timestamp=300,
    )
    assert len(qs.queue) == 3
    assert qs.active_montage_id == "roi2"
    assert qs.completed_count == 1


def test_queue_status_roundtrip():
    qs = QueueStatus(
        queue=[
            ROIStatus(montage_id="test", status=ROIEntryStatus.PENDING, timestamp=100)
        ],
        completed_count=0,
        timestamp=200,
    )
    restored = QueueStatus(**qs.model_dump())
    assert len(restored.queue) == 1
    assert restored.queue[0].montage_id == "test"


def test_queue_update_remove():
    qu = QueueUpdate(remove=["montage_1", "montage_2"])
    assert qu.remove == ["montage_1", "montage_2"]
    assert qu.reorder is None


def test_queue_update_reorder():
    qu = QueueUpdate(reorder=["montage_3", "montage_1", "montage_2"])
    assert qu.reorder == ["montage_3", "montage_1", "montage_2"]
    assert qu.remove is None


def test_queue_update_remove_and_reorder():
    qu = QueueUpdate(remove=["montage_1"], reorder=["montage_3", "montage_2"])
    assert qu.remove == ["montage_1"]
    assert qu.reorder == ["montage_3", "montage_2"]


def test_create_roi_overlap_optional():
    roi = CreateROI(
        vertices=[Vertex(x=0, y=0), Vertex(x=100, y=100)],
        rotation_angle=0.0,
        montage_id="test",
    )
    assert roi.overlap is None


def test_create_roi_overlap_set():
    roi = CreateROI(
        vertices=[Vertex(x=0, y=0), Vertex(x=100, y=100)],
        rotation_angle=0.0,
        montage_id="test",
        overlap=25,
    )
    assert roi.overlap == 25


def test_create_roi_overlap_validation():
    with pytest.raises(Exception):
        CreateROI(
            vertices=[Vertex(x=0, y=0), Vertex(x=100, y=100)],
            rotation_angle=0.0,
            montage_id="test",
            overlap=150,
        )
    with pytest.raises(Exception):
        CreateROI(
            vertices=[Vertex(x=0, y=0), Vertex(x=100, y=100)],
            rotation_angle=0.0,
            montage_id="test",
            overlap=-5,
        )


def test_calibration_ops_defaults_all_false():
    ops = CalibrationOptions()
    assert ops.auto_focus is False
    assert ops.auto_exposure is False
    assert ops.lens_correction is False
    assert ops.bright_field is False
    assert ops.dark_field is False
    assert ops.beam_center is False
    assert ops.beam_spread is False
    assert ops.find_aperture is False
    assert ops.calibrate_resolution is False


def test_calibration_ops_settable():
    ops = CalibrationOptions(auto_focus=True, beam_center=True)
    assert ops.auto_focus is True
    assert ops.beam_center is True
    assert ops.auto_exposure is False


def test_tilt_calibration_ops_only_tilt_specific_fields():
    tilt_fields = set(TiltCalibrationOptions.model_fields)
    assert tilt_fields == {
        "eucentric_height",
        "track_feature",
        "beam_tilt_compensation",
    }


def test_tilt_calibration_ops_defaults_all_true():
    tcf = TiltCalibrationOptions()
    assert tcf.eucentric_height is True
    assert tcf.track_feature is True
    assert tcf.beam_tilt_compensation is True


def test_tilt_calibration_ops_opt_out():
    tcf = TiltCalibrationOptions(eucentric_height=False)
    assert tcf.eucentric_height is False
    assert tcf.track_feature is True  # default preserved
    assert tcf.beam_tilt_compensation is True


def _square_vertices():
    return [Vertex(x=0, y=0), Vertex(x=10, y=0), Vertex(x=10, y=10), Vertex(x=0, y=10)]


def test_roi_acquisition_type_default_is_montage():
    roi = CreateROI(
        vertices=_square_vertices(),
        rotation_angle=0.0,
        montage_id="m1",
    )
    assert roi.acquisition_type == AcquisitionType.MONTAGE


def test_roi_calibrations_default_empty():
    roi = CreateROI(
        vertices=_square_vertices(),
        rotation_angle=0.0,
        montage_id="m1",
    )
    assert roi.calibrations.auto_focus is False
    assert roi.calibrations.auto_exposure is False


def test_roi_tilt_calibrations_default_none():
    roi = CreateROI(
        vertices=_square_vertices(),
        rotation_angle=0.0,
        montage_id="m1",
    )
    assert roi.tilt_calibrations is None


def test_tilt_calibrations_only_valid_for_tilt_series():
    with pytest.raises(ValidationError):
        CreateROI(
            vertices=_square_vertices(),
            rotation_angle=0.0,
            montage_id="m1",
            acquisition_type=AcquisitionType.MONTAGE,
            tilt_calibrations={"eucentric_height": True},
        )


def test_tilt_calibrations_rejected_on_lens_correction():
    with pytest.raises(ValidationError):
        CreateROI(
            vertices=_square_vertices(),
            rotation_angle=0.0,
            montage_id="m1",
            acquisition_type=AcquisitionType.LENS_CORRECTION,
            tilt_calibrations={"eucentric_height": True},
        )


def test_tilt_calibrations_rejected_on_survey():
    with pytest.raises(ValidationError):
        CreateROI(
            vertices=_square_vertices(),
            rotation_angle=0.0,
            montage_id="m1",
            acquisition_type=AcquisitionType.SURVEY,
            tilt_calibrations={"eucentric_height": True},
        )


def test_tilt_calibrations_accepted_on_tilt_series():
    roi = CreateROI(
        vertices=_square_vertices(),
        rotation_angle=0.0,
        montage_id="m1",
        acquisition_type=AcquisitionType.TILT_SERIES,
        tilt_angles=[-10.0, 0.0, 10.0],
        tilt_calibrations={"eucentric_height": False},
    )
    assert roi.tilt_calibrations.eucentric_height is False
    assert roi.tilt_calibrations.track_feature is True
    assert roi.tilt_calibrations.beam_tilt_compensation is True


def test_tilt_series_requires_multiple_tilt_angles():
    with pytest.raises(ValidationError):
        CreateROI(
            vertices=_square_vertices(),
            rotation_angle=0.0,
            montage_id="m1",
            acquisition_type=AcquisitionType.TILT_SERIES,
            tilt_angles=[0.0],
        )


def test_tilt_series_accepts_multiple_tilt_angles():
    roi = CreateROI(
        vertices=_square_vertices(),
        rotation_angle=0.0,
        montage_id="m1",
        acquisition_type=AcquisitionType.TILT_SERIES,
        tilt_angles=[-10.0, 0.0, 10.0],
    )
    assert roi.acquisition_type == AcquisitionType.TILT_SERIES


def test_lens_correction_rejects_multiple_tilt_angles():
    with pytest.raises(ValidationError):
        CreateROI(
            vertices=_square_vertices(),
            rotation_angle=0.0,
            montage_id="m1",
            acquisition_type=AcquisitionType.LENS_CORRECTION,
            tilt_angles=[-10.0, 0.0, 10.0],
        )


def test_lens_correction_accepts_default_or_zero_angle():
    roi = CreateROI(
        vertices=_square_vertices(),
        rotation_angle=0.0,
        montage_id="m1",
        acquisition_type=AcquisitionType.LENS_CORRECTION,
    )
    assert roi.acquisition_type == AcquisitionType.LENS_CORRECTION


def test_survey_rejects_multiple_tilt_angles():
    with pytest.raises(ValidationError):
        CreateROI(
            vertices=_square_vertices(),
            rotation_angle=0.0,
            montage_id="m1",
            acquisition_type=AcquisitionType.SURVEY,
            tilt_angles=[-10.0, 0.0, 10.0],
        )


def test_roi_serialize_deserialize_round_trip():
    roi = CreateROI(
        vertices=_square_vertices(),
        rotation_angle=0.0,
        montage_id="m1",
        acquisition_type=AcquisitionType.LENS_CORRECTION,
        calibrations={"auto_focus": True},
    )
    payload = roi.model_dump()
    assert payload["acquisition_type"] == "lens_correction"
    restored = CreateROI(**payload)
    assert restored.acquisition_type == AcquisitionType.LENS_CORRECTION
    assert restored.calibrations.auto_focus is True
