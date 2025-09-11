from pigeon import BaseMessage
from pydantic import Field


class Status(BaseMessage):
    """
    This message contains information about the status of the tile upload buffer.
    """

    queue_length: int = Field(
        description="The number of tiles currently stored and waiting to be uploaded."
    )
    free_space: int = Field(
        description="The amount of free space on the tile storage disk in bytes."
    )
    upload_rate: int = Field(
        description="The rate at which data is being uploaded in bits per second."
    )
