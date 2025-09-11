from pigeon import BaseMessage


class Current(BaseMessage):
    state: str


class Change(BaseMessage):
    previous: str
    current: str
