from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from db.schemas.relation_schemas import User


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    image: Optional[bytes] = None

    date_posted: datetime
    date_updated: datetime
    author: User

    class Config:
        orm_mode = True
