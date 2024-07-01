from io import BytesIO
from typing import List, Optional

from fastapi import HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from db.models import DbBlogPost
from db.schemas import PostIn, PostOut

Error_404 = HTTPException(status_code=404, detail="Not found.")
Error_integrity = HTTPException(
    400, detail="Update failed due to integrity constraint violation"
)


async def create_post(post: PostIn, image: Optional[UploadFile], db: Session) -> PostOut:
    image_content = await image.read() if image else None

    new_post = DbBlogPost(
        title=post.title,
        content=post.content,
        author=post.author,
        image=image_content,
    )
    try:
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return PostOut.from_db_post(new_post)
    except IntegrityError:
        db.rollback()
        raise Error_integrity


def delete_post(post_id: int, db: Session) -> PostOut:
    try:
        post = db.query(DbBlogPost).get(post_id)

        db.delete(post)
        db.commit()
        return PostOut.from_db_post(post)
    except NoResultFound:
        raise Error_404


def get_post(post_id: int, db: Session) -> PostOut:
    try:
        post = db.query(DbBlogPost).get(post_id)
        return PostOut.from_db_post(post)
    except NoResultFound:
        raise Error_404


def get_post_image(post_id, db) -> StreamingResponse:
    try:
        post = db.query(DbBlogPost).get(post_id)
    except NoResultFound:
        raise Error_404
    if not post.image:
        raise Error_404
    return StreamingResponse(BytesIO(post.image), media_type="image/png")


async def update_post(
    input_data: dict, image: Optional[UploadFile], post_id: int, db: Session
) -> PostOut:
    try:
        existing_post = db.query(DbBlogPost).get(post_id)

        if title := input_data.get("title", None):
            existing_post.title = title
        if content := input_data.get("content", None):
            existing_post.content = content
        if author := input_data.get("author", None):
            existing_post.author = author

        if image:
            image_content = await image.read()
            existing_post.image = image_content

        db.commit()
        db.refresh(existing_post)
        return PostOut.from_db_post(existing_post)
    except NoResultFound:
        raise Error_404
    except IntegrityError:
        db.rollback()
        raise Error_integrity


async def upload_image(post_id: int, image: UploadFile, db: Session):
    try:
        existing_post = db.query(DbBlogPost).get(post_id)

        image_content = await image.read()
        existing_post.image = image_content

        db.commit()
        db.refresh(existing_post)
        return PostOut.from_db_post(existing_post)
    except NoResultFound:
        raise Error_404
    except IntegrityError:
        db.rollback()
        raise Error_integrity


def get_posts(db: Session) -> List[PostOut]:
    posts = db.query(DbBlogPost).all()
    return [PostOut.from_db_post(post) for post in posts]
