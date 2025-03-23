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
