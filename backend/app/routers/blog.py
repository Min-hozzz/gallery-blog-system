from datetime import datetime
from operator import truediv

from fastapi import APIRouter, Depends,HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select

from ..dependencies import get_db, get_current_user
from ..models.blog import Post
from ..models.user import User

from ..schemas.blog import PostResponse, PostCreate, PostUpdate

router = APIRouter(tags=["blog"])

# 创建博客
@router.post("/posts",response_model=PostResponse)
async def create_post(
        post: PostCreate,
        db:AsyncSession = Depends(get_db)
):
    db_post = Post(**post.model_dump())
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post

# id 指定博客
@router.get("/posts/{post_id}",response_model=PostResponse)
async def read_post(
        post_id: int,
        db:AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Post)
        .where(Post.id == post_id)
        .where(Post.is_deleted == False)  # 关键过滤条件
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(404, "文章不存在或已被删除")
    return post


# 更新博客
@router.put("/posts/{post_id}",response_model=PostResponse)
async def update_post(
        post_id: int,
        post_update: PostUpdate,
        db:AsyncSession = Depends(get_db)
):
    # 根据id找到post并更新post
    result = await db.execute(
        select(Post).where(Post.id == post_id)
    )
    db_post = result.scalar_one_or_none()

    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # update
    update_data = post_update.model_dump(exclude_unset=True)
    for field , value in update_data.items():
        setattr(db_post, field, value)

    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post

# 软删除
@router.delete("/posts/{post_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
        post_id: int,
        current_user : User = Depends(get_current_user),
        db:AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Post).where(Post.id == post_id)
    )
    db_post = result.scalar_one_or_none()

    if not db_post:
        raise HTTPException(404, "文章不存在")
    if db_post.author_id != current_user.id:
        raise HTTPException(403, "无权删除此文章")

        # 执行软删除
    db_post.is_deleted = True
    db_post.deleted_at = datetime.utcnow()
    await db.commit()
    return {"message": "文章已移至回收站"}

# 回收路由
@router.get("/trash",response_model=list[PostResponse])
async def list_deleted_post(
        db:AsyncSession = Depends(get_db),
        current_user : User = Depends(get_current_user)
):
    # 查看已软删除的文章
    res = await db.execute(
        select(Post)
        .where(Post.author_id == current_user.id)
        .where(Post.is_deleted == True)
    )
    return res.scalars().all()



# 恢复文章
router.post("/post/{post_id}/restore")
async def restore_post(
        post_id: int,
        db:AsyncSession = Depends(get_db),
        current_user : User = Depends(get_current_user)
):
    res = await db.execute(
        select(Post)
        .where(Post.id == post_id)
        .where(Post.is_deleted == True)
    )
    post = res.scalar_one_or_none()
    if not post:
        raise HTTPException(404,"post not found")
    if post.author_id != current_user.id:
        raise HTTPException(403,"not authorized")
    post.is_deleted = False
    post.deleted_at = None
    await db.commit()
    return {"message": "had restored"}