from fastapi import APIRouter, Path, Depends
from db.database_definition import get_db

router = APIRouter(
    prefix="/blogpost",
    tags=["blog"],
)


@router.post("/", response_model=PostDisplay)
async def create_post(
    request: PostBase,
    db: Session = Depends(get_db),
    current_user: UserBase = Depends(get_current_user),
):
    return await db_post.create_post(db, request)
