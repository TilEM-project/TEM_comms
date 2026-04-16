import pytest
from TEM_comms.roi import (
    ROIEntryStatus,
    ROIStatus,
    QueueStatus,
    QueueUpdate,
    CreateROI,
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
