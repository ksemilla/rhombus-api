from ninja import Schema

class IngestOut(Schema):
    id: int
    name: str
    status: str
    file: str
    process_time: float
    row_nums: int
    processed_row_nums: int

class ColumnOut(Schema):
    id: int
    label: str
    value: str
    dtype:  str
    display_order: int

class ColumnIn(Schema):
    label: str = None
    dtype:  str = None

class RecordOut(Schema):
    id: int
    data: dict