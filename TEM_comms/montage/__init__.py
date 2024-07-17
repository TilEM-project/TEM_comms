from pigeon import BaseMessage


class Start(BaseMessage):
    montage_id: str
    num_tiles: int


class Finished(BaseMessage):
    montage_id: str
    num_tiles: int
    roi: str
    specimen: str
    metadata_file_path: str
