from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    assigned_to: int
    status: Optional[str] = None


class TaskUpdate(BaseModel):
    status: Optional[str] = None
    description: Optional[str] = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    assigned_to: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
