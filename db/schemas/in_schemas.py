from typing import Optional

from pydantic import BaseModel


class PostIn(BaseModel):
    title: str
    content: str
    image: Optional[bytes] = None
    author_id: int


# Unused vvvv
class UserIn(BaseModel):
    name: str


# Unused vvvv
class ImageIn(BaseModel):
    image: bytes
