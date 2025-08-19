from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel  # 新增Pydantic模型导入
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import select

from ..dependencies import get_db
from ..models.user import User
from ..schemas.user import UserCreate
from ..services import auth
from ..services.auth import authenticate_user

router = APIRouter(tags=["auth"])

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# ---------- 安全配置 ----------
SECRET_KEY = "52d6bfec29b5efde4b09bf122cf2c2b33e39970e5c4167148eaf85bbec04057c"  # 生产环境应从环境变量读取
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ---------- 工具初始化 ----------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ---------- 模拟用户数据库 ----------
fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("secret"),  # 密码已加密
    }
}

@router.post("/register")
async def register(
        user: UserCreate,
        db: AsyncSession = Depends(get_db)):
    # 检查用户名是否已存在
    result = await db.execute(
        select(User).where(User.username == user.username)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(400, "用户名已存在")

    # 创建用户（不涉及邮箱验证）
    db_user = User(
        username=user.username,
        email=user.email,  # 可选字段
        hashed_password=pwd_context.hash(user.password),
        is_active=True
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


# ---------- 核心路由 ----------
@router.post("/login")
async def login(
        credentials: LoginRequest,
        db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(401, "用户名或密码错误")
    access_token = create_access_token(credentials.username)
    return {"access_token": access_token, "token_type": "bearer"}

def create_access_token(username: str) -> str:
    """生成JWT令牌"""
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": username,
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)