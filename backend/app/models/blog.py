from datetime import datetime

from sqlalchemy import Column,Integer,String,Text,DateTime

from .base import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True,index=True)
    title = Column(String(100),nullable=False)
    content = Column(Text)
    created_at = Column(DateTime,default=datetime.now())


