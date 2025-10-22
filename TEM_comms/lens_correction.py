from pigeon import BaseMessage
from pydantic import Field


class Transform(BaseMessage):
    """
    This message contains a compact representation of the generated lens correction transform.
    """

    transform: str = Field(description="The base64 encoded lens correction transform.")
