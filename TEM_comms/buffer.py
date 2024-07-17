from pigeon import BaseMessage


class Status(BaseMessage):
    queue_length: int
    free_space: int
    upload_rate: int
