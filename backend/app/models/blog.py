from datetime import datetime

from sqlalchemy import Column,Integer,String,Text,DateTime
from sqlalchemy.sql.sqltypes import Boolean

from .base import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True,index=True)
    title = Column(String(100),nullable=False)
    content = Column(Text)
    author_id = Column(Integer)
    created_at = Column(DateTime,default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)  # 软删除标记
    deleted_at = Column(DateTime, nullable=True)  # 删除时间



