from .base import BaseMessage

class status(BaseMessage):
    queue_length: int
    free_space: int
    upload_rate: int