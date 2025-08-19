from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.sqltypes import Text

from .base import Base


class GalleryImage(Base):
    __tablename__ = "gallery_images"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String(500),nullable=False)
    description = Column(Text)
    uploader_id = Column(Integer, index=True)
    uploaded_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),  # 与数据库DEFAULT同步
        nullable=False)
    location = Column(String(50))  # 存储 "POINT(lng lat)"