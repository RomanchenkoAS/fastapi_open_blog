from datetime import datetime

from pydantic import BaseModel


class Post(BaseModel):
    # Post inside UserDisplay
    title: str
    date_posted: datetime

    class Config:
        orm_mode = True


class User(BaseModel):
    # Author inside PostDisplay
    name: str

    class Config:
        orm_mode = True
