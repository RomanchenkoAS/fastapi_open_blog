from typing import Optional

from pydantic import BaseModel


class PostIn(BaseModel):
    title: str
    content: str
    image: Optional[bytes] = None
    author_id: int


class UserIn(BaseModel):
    name: str


class ImageIn(BaseModel):
    image: bytes
