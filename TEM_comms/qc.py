from pigeon import BaseMessage
from typing import Literal


class Status(BaseMessage):
    state: Literal["GOOD", "STOP_AT_END", "STOP_NOW"]
