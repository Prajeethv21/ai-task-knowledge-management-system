from datetime import datetime

from pydantic import BaseModel


class DocumentOut(BaseModel):
    id: int
    filename: str
    original_name: str
    content_type: str
    size: int
    chunk_count: int
    uploaded_by: int
    uploaded_at: datetime

    class Config:
        from_attributes = True
