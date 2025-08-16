from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..models.blog import Post
from backend.app.schemas.blog import PostResponse, PostCreate

router = APIRouter(prefix="/posts",tags=["blog"])

@router.get("/",response_model=PostResponse)
async def create_post(post: PostCreate, db:Session = Depends(get_db)):
    db_post = Post(**post.dict())
    db.add(db_post)
    db.commit()
    return db_post
