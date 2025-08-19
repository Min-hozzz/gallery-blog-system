import os
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, gallery,blog  # 确保导入auth路由
app = FastAPI()
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))


os.environ["TZ"] = "Asia/Shanghai"
time.tzset()  # Linux/macOS生效
# 添加CORS中间件（必须放在路由注册前）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 精确匹配前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)  # 注册路由
app.include_router(gallery.router, prefix="/gallery") # 关键！前缀匹配
app.include_router(blog.router, prefix="/blog")
@app.get("/")
def read_root():
    return {"message": "come to fast api"}
