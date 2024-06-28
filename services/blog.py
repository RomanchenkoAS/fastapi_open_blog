from base64 import b64encode
from typing import Any, List, Optional

from fastapi import HTTPException
from fastapi import UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from db.models import DbBlogPost
from db.schemas import PostIn, PostOut


async def create_post(
    post: PostIn, image: Optional[UploadFile], db: Session
) -> DbBlogPost:
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
        return new_post
    except IntegrityError:
        db.rollback()
        raise HTTPException(400, detail="Post already exists.")


def delete_post(post_id: int, db: Session) -> dict[str, Any]:
    raise NotImplementedError()


def get_post(post_id: int, db: Session) -> PostOut:
    try:
        post = db.query(DbBlogPost).get(post_id)
    except NoResultFound:
        raise HTTPException(404, detail="Post was not found.")

    # Convert image bytes to base64-encoded string
    image_str = None
    if post.image:
        image_str = b64encode(post.image).decode("utf-8")

    return PostOut(
        id=post.id,
        title=post.title,
        content=post.content,
        image=image_str,
        date_posted=post.date_posted,
        date_updated=post.date_updated,
        author=post.author,
    )


def update_post(new_post: PostIn, post_id: int, db: Session) -> PostOut:
    raise NotImplementedError()


def get_posts(db: Session) -> List[PostOut]:
    raise NotImplementedError()


def upload_image(post_id: int, uploaded_file: UploadFile, db: Session):
    raise NotImplementedError()


# def get_author_id(author_name: str, db: Session) -> int:
#     try:
#         author = db.query(DbAuthor).filter_by(name=author_name).one()
#     except NoResultFound:
#         author = create_author(author_name, db)
#     return author.id
#
#
# def create_author(author_name: str, db: Session) -> DbAuthor:
#     new_author = DbAuthor(name=author_name, is_admin=False)
#     try:
#         db.add(new_author)
#         db.commit()
#         db.refresh(new_author)
#     except Exception as e:
#         db.rollback()
#         raise e
#     return new_author
#
#
# def update_author(author_id: int, db: Session) -> None:
#     try:
#         author = db.query(DbAuthor).get(author_id)
#         author.last_posted = datetime.now()
#         db.commit()
#         db.refresh(author)
#     except Exception as e:
#         db.rollback()
#         raise e
