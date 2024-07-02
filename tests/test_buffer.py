import re

import pytest
from TEM_comms.buffer import Status

from pydantic import ValidationError


# Test cases for the Status class
@pytest.mark.parametrize(
    "queue_length, free_space, upload_rate, test_id",
    [
        (10, 100, 20, "test_id_01"),  # Happy path: normal values
        (0, 0, 0, "test_id_02"),  # Edge case: zero values
        (100, 500, 100, "test_id_03"),  # Happy path: higher values
        (-1, -100, -10, "test_id_04"),  # Error case: negative values
        (1e6, 1e6, 1e4, "test_id_05"),  # Edge case: very large values
    ],
)
def test_status_initialization(queue_length, free_space, upload_rate, test_id):
    # Act
    status = Status(
        queue_length=queue_length, free_space=free_space, upload_rate=upload_rate
    )

    # Assert
    assert (
        status.queue_length == queue_length
    ), f"{test_id}: queue_length does not match"
    assert status.free_space == free_space, f"{test_id}: free_space does not match"
    assert status.upload_rate == upload_rate, f"{test_id}: upload_rate does not match"


# Test cases for handling type errors
@pytest.mark.parametrize(
    "queue_length, free_space, upload_rate, test_id",
    [
        (
            "ten",
            100,
            20,
            "test_id_06",
        ),  # Error case: string instead of int for queue_length
        (
            10,
            "hundred",
            20,
            "test_id_07",
        ),  # Error case: string instead of int for free_space
        (
            10,
            100,
            "twenty",
            "test_id_08",
        ),  # Error case: string instead of int for upload_rate
    ],
)
def test_status_type_errors(queue_length, free_space, upload_rate, test_id):
    # Act and Assert
    expected_error_pattern = re.escape("validation error")
    with pytest.raises(ValidationError, match=expected_error_pattern):
        Status(
            queue_length=queue_length, free_space=free_space, upload_rate=upload_rate
        )
