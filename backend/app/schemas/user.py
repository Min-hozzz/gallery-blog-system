from pydantic import BaseModel,EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr | None = None

class UserCreate(UserBase):
    password: str # 创建时明文密码

class UserInDB(UserBase):
    id: int
    is_active : bool

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    username: str | None = None