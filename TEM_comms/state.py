from pigeon import BaseMessage
from pydantic import Field


class Current(BaseMessage):
    """
    This message contains the current state of the orchastration state machine.
    """

    state: str = Field(
        description="The current state of the orchastration state machine."
    )


class Change(BaseMessage):
    """
    This message is sent on a state change of the orchastration state machine.
    """

    old: str = Field(
        description="The previous state of the orchastration state machine."
    )
    new: str = Field(description="The new state of the orchastration state machine.")
