from typing import List

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from db.database_definition import get_db
from db.schemas.in_schemas import PostIn
from db.schemas.out_schemas import PostOut
from services import blog

router = APIRouter(
    prefix="/blogpost",
    tags=["blog"],
)


@router.post("/", response_model=PostOut)
async def create_post(new_post: PostIn, db: Session = Depends(get_db)):
    return blog.create_post(new_post)


@router.get("/", response_model=List[PostOut])
async def get_posts(db: Session = Depends(get_db)):
    return blog.get_posts()


@router.get("/{id}", response_model=PostOut)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    return blog.get_post(post_id)


@router.delete("/{id}")
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    return blog.delete_post(post_id)


@router.patch("/{id}", response_model=PostOut)
async def update_post(new_post: PostIn, post_id: int, db: Session = Depends(get_db)):
    return blog.update_post(new_post, post_id)


@router.post("/{id}/upload")
async def upload_image(uploaded_file: UploadFile = File(...)):
    return blog.upload_image(uploaded_file)
