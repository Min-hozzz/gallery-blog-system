from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth  # 确保导入auth路由
app = FastAPI()

# 添加CORS中间件（必须放在路由注册前）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 精确匹配前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)  # 注册路由

@app.get("/")
def read_root():
    return {"message": "come to fast api"}
