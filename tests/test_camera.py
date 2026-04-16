from TEM_comms.camera import Command
from pytest import mark


@mark.parametrize(
    "data",
    [
        {
            "montage_id": "a montage id",
            "tile_id": "a tile id",
            "row": 1,
            "column": 2,
            "overlap": 100,
        },
        {
            "montage_id": "a montage id",
            "tile_id": "a tile id",
            "row": 1,
            "column": 2,
            "overlap": 100,
            "darkfield": True,
        },
        {
            "montage_id": "a montage id",
            "tile_id": "a tile id",
            "row": 1,
            "column": 2,
            "overlap": 100,
            "brightfield": True,
        },
        {
            "montage_id": "a montage id",
            "tile_id": "a tile id",
            "row": 1,
            "column": 2,
            "overlap": 100,
            "lens_correction": False,
        },
    ],
)
def test_command(data):
    Command(**data)


def test_command_with_roi_id():
    cmd = Command(
        montage_id="ROI_4_20260413T205135_p15.0",
        tile_id="a tile id",
        row=1,
        column=2,
        overlap=100,
        roi_id="ROI_4_20260413T205135",
    )
    assert cmd.roi_id == "ROI_4_20260413T205135"


def test_command_without_roi_id_defaults_none():
    cmd = Command(
        montage_id="a montage id",
        tile_id="a tile id",
        row=1,
        column=2,
        overlap=100,
    )
    assert cmd.roi_id is None
