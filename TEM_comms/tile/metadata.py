from pigeon import BaseMessage


class TileMetadata(BaseMessage):
    tile_id: str
    montage_id: str
    row: int
    column: int
    overlap: int
