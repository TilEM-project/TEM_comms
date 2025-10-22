from TEM_comms.tile import Matches


def test_matches_empty():
    matches = Matches(
        row=2,
        column=5,
        overlap=128,
        tile_id="a_tile_id",
        montage_id="a_montage_id",
        matches=(),
    )


def test_matches():
    matches = Matches(
        row=2,
        column=5,
        overlap=128,
        tile_id="a_tile_id",
        montage_id="a_montage_id",
        matches=(
            {
                "row": 3,
                "column": 5,
                "dX": 24.3,
                "dY": 37.8,
                "distance": 55.7,
                "rotation": 0.1,
                "position": "bottom",
                "dXsd": 0.47,
                "dYsd": 0.35,
                "pX": [1, 2, 3, 4],
                "pY": [5, 6, 7, 8],
                "qX": [9, 10, 11, 12],
                "qY": [13, 14, 15, 16],
            },
            {
                "row": 2,
                "column": 6,
                "dX": 14.9,
                "dY": 32.3,
                "distance": 42.1,
                "rotation": -0.04,
                "position": "right",
                "dXsd": 0.59,
                "dYsd": 0.21,
                "pX": [4, 3, 2, 1],
                "pY": [8, 7, 6, 5],
                "qX": [12, 11, 10, 9],
                "qY": [16, 15, 14, 13],
            },
        ),
    )
