# backend/app/db_init.py
from .models.base import Base
from .dependencies import sync_engine

# !/usr/bin/env python3
"""
数据库表初始化脚本
执行命令：python -m app.db_init
"""

import sys
from sqlalchemy import create_engine
from sqlalchemy.inspection import inspect

# 解决模块导入问题
sys.path.append("/home/homan/project/gallery-blog-system/backend")

from .models.base import Base
from .models.user import User
from .models.blog import Post
from .dependencies import SYNC_DB_URL  # 同步数据库URL


def init_db():
    """初始化数据库表结构"""
    try:
        # 创建引擎（同步模式）
        engine = create_engine(
            SYNC_DB_URL,
            echo=True,  # 打印SQL日志
            pool_pre_ping=True,
            pool_recycle=3600
        )

        print(f"🔗 正在连接数据库: {engine.url.database}")

        # 创建所有表
        Base.metadata.drop_all(bind=engine)

        # 按顺序创建表
        User.__table__.create(bind=engine)  # 先创建users
        Post.__table__.create(bind=engine)  # 再创建posts

        # 验证表是否创建成功
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print("✅ 已创建的表:", tables)

        if not tables:
            raise RuntimeError("表创建失败，请检查数据库权限")

    except Exception as e:
        print("❌ 初始化失败:", str(e))
        sys.exit(1)


if __name__ == "__main__":
    init_db()