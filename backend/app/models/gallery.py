from sqlalchemy import Column, Integer, String, DateTime


from .base import Base


class GalleryImage(Base):
    __tablename__ = "gallery_images"

    id = Column(Integer, primary_key=True)
    image_url = Column(String(500))
    uploaded_at = Column(DateTime(timezone=True))
    location = Column(String(50))  # 存储 "POINT(lng lat)"