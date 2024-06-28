from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from db.models import DbBlogPost


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

    @classmethod
    def from_db_post(cls, db_post: DbBlogPost) -> "PostOut":
        return cls(
            id=db_post.id,
            title=db_post.title,
            content=db_post.content,
            date_posted=db_post.date_posted,
            date_updated=db_post.date_updated,
            author=db_post.author if db_post.author else None,
            image_url=f"/blogposts/{db_post.id}/image" if db_post.image else None,
        )


class Post(BaseModel):
    title: str
    date_posted: datetime

    class Config:
        orm_mode = True
