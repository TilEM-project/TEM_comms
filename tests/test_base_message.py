from TEM_comms.msgs.base import BaseMessage
import json
from pydantic import ValidationError
import pytest


class Msg(BaseMessage):
    x: int
    y: int


def test_serialize():
    data = {"x": 1, "y": 2}
    msg = Msg(**data)

    assert json.loads(msg.serialize()) == data


def test_deserialize():
    data = {"x": 3, "y": 4}
    msg = Msg.deserialize(json.dumps(data))

    assert msg.x == data["x"]
    assert msg.y == data["y"]


def test_forbid_extra():
    with pytest.raises(ValidationError):
        Msg(x=1, y=2, z=3)
    with pytest.raises(ValidationError):
        Msg.deserialize(json.dumps({"x": 1, "y": 2, "z": 3}))


def test_mising_values():
    with pytest.raises(ValidationError):
        Msg(x=1)
    with pytest.raises(ValidationError):
        Msg.deserialize(json.dumps({"y": 3}))
