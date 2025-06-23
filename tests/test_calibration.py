from TEM_comms.calibration import Resolution
import pytest
import json


@pytest.mark.parametrize(
    "data",
    [
        {
            "mag": {},
            "lowmag": {},
        },
        {
            "mag": {},
            "lowmag": {50: {"nm_per_px": (180.4, 170.6), "rotation": 3.14}},
        },
        {
            "mag": {3000: {"nm_per_px": (4.5, 4.7), "rotation": 1.5}},
            "lowmag": {},
        },
        {
            "mag": {3000: {"nm_per_px": (4.5, 4.7), "rotation": 1.5}},
            "lowmag": {50: {"nm_per_px": (180.4, 170.6), "rotation": 3.14}},
        },
        {
            "mag": {
                3000: {"nm_per_px": (4.5, 4.7), "rotation": 1.5},
                1500: {"nm_per_px": (7.1, 7.3), "rotation": 2.1},
            },
            "lowmag": {50: {"nm_per_px": (180.4, 170.6), "rotation": 3.14}},
        },
    ],
)
def test_calibration(data):
    msg = Resolution(**data)
    assert Resolution.deserialize(msg.serialize()) == msg
