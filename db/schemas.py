from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PostIn(BaseModel):
    title: str
    content: str
    author: str


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    date_posted: datetime
    date_updated: datetime
    author: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        orm_mode = True


class Post(BaseModel):
    title: str
    date_posted: datetime

    class Config:
        orm_mode = True
