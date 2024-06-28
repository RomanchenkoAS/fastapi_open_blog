from typing import List

from fastapi import APIRouter, File, UploadFile, Depends, Form
from sqlalchemy.orm import Session

from db.database_definition import get_db
from db.schemas import PostIn, PostOut
from services import blog

router = APIRouter(
    prefix="/blogpost",
    tags=["blog"],
)


@router.post("/", response_model=PostOut)
async def create_post(
    title: str = Form(...),
    content: str = Form(...),
    author: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    post_in = PostIn(itle=title, content=content, author=author)
    post_out = await blog.create_post(post_in, image, db)
    return post_out


@router.get("/{post_id}", response_model=PostOut)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    return blog.get_post(post_id, db)


@router.get("/", response_model=List[PostOut])
async def get_posts(db: Session = Depends(get_db)):
    return blog.get_posts(db)


@router.delete("/{post_id}")
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    return blog.delete_post(post_id, db)


@router.patch("/{post_id}", response_model=PostOut)
async def update_post(request: PostIn, post_id: int, db: Session = Depends(get_db)):
    return blog.update_post(request, post_id, db)


@router.post("/{post_id}/upload")
async def upload_image(
    post_id: int, uploaded_file: UploadFile = File(...), db: Session = Depends(get_db)
):
    return blog.upload_image(post_id, uploaded_file, db)
