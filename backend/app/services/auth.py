from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select

from ..models.user import pwd_context, User
from ..schemas.user import UserCreate, UserInDB


def get_user(db: Session,username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_active=True,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def authenticate_user(
        db: AsyncSession,
        username: str,
        password: str | None
) -> User | None:
    result = await db.execute(
        select(User).where(User.username == username)
    )
    user = result.scalar_one_or_none()

    if password is not None:
        if not user or not pwd_context.verify(password, user.hashed_password):
            return None
    return user