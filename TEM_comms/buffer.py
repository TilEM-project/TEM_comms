from pigeon import BaseMessage


class Status(BaseMessage):
    montage_id: str
    queue_length: int
    free_space: int
    upload_rate: int
