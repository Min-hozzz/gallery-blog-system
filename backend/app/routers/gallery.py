from fastapi import APIRouter, UploadFile, File,Form, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio.session import AsyncSession

from ..models.gallery import GalleryImage
from ..dependencies import get_db
import shutil
import os


router = APIRouter(tags=["gallery"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_image(
        file: UploadFile = File(...),
        uploader_id: int = Form(...),
        db: AsyncSession = Depends(get_db)
):
    # 保存文件到本地（生产环境建议用云存储）
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # 记录到数据库
    db_image = GalleryImage(
        image_url=file_path,
        uploader_id=uploader_id,
        location="POINT(0 0)"  # 默认位置
    )
    db.add(db_image)
    await db.commit()
    return {"url": file_path}