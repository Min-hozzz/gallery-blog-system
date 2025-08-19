from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class BlogBase(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class PostCreate(BlogBase):
    title: str
    content: str
    author_id: int

class PostUpdate(BlogBase):
    pass

class PostResponse(PostCreate):
    id: int
    created_at: datetime
    updated_at: datetime | None
    class Config:
        orm_mode = True