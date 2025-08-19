from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from sqlalchemy.pool import NullPool

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select

from backend.app.routers.auth import oauth2_scheme, SECRET_KEY, ALGORITHM
from models.user import User
from schemas.user import TokenData
from datetime import datetime

# 同步引擎（建表用）
sync_engine = create_engine(
    "mysql+pymysql://project-database:zzt980815@124.71.4.24/project-database",
    pool_recycle=3600,  # 1小时重新连接
    pool_pre_ping=True, # 执行前检查连接
    connect_args={
        "connect_timeout": 10,  # 连接超时10秒
    }
)

# 异步引擎（API用）
async_engine = create_async_engine(
    "mysql+asyncmy://project-database:zzt980815@124.71.4.24/project-database",
    pool_recycle=3600,
    pool_pre_ping=True,
    poolclass=NullPool  # 禁用连接池（适合开发环境）
)

# 同步引擎（迁移用）
# sync_engine = create_engine("mysql+pymysql://project-database:zzt980815@124.71.4.24/project-database")

# 异步引擎（API用）
# async_engine = create_async_engine("mysql+asyncmy://project-database:zzt980815@124.71.4.24/project-database")
AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# 同步数据库URL（建表用）
SYNC_DB_URL = "mysql+pymysql://project-database:zzt980815@124.71.4.24/project-database"

# 异步数据库URL（API用）
ASYNC_DB_URL = "mysql+asyncmy://project-database:zzt980815@124.71.4.24/project-database"


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
) -> User:
    """解析JWT并获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 1. 解码JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    # 2. 异步查询用户
    result = await db.execute(
        select(User)
        .where(User.username == token_data.username)
        .where(User.is_active == True)  # 确保用户未禁用
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    # 3. 检查软删除状态（可选）
    if hasattr(user, 'is_deleted') and user.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="用户账号已被删除"
        )

    return user