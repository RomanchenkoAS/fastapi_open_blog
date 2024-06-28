from typing import Any, List

from fastapi import UploadFile

from db.schemas.in_schemas import PostIn
from db.schemas.out_schemas import PostOut


def create_post(new_post: PostIn) -> PostOut:
    raise NotImplementedError()


def delete_post(post_id: int) -> dict[str, Any]:
    raise NotImplementedError()


def get_post(post_id: int) -> PostOut:
    raise NotImplementedError()


def update_post(new_post: PostIn, post_id: int) -> PostOut:
    raise NotImplementedError()


def get_posts() -> List[PostOut]:
    raise NotImplementedError()


def upload_image(uploaded_file: UploadFile):
    raise NotImplementedError()


def create_author():
    raise NotImplementedError()


def update_author():
    raise NotImplementedError()
