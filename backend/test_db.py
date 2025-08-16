from sqlalchemy.sql.expression import text

from app.utils.database import engine

if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            print("✅ 数据库连接成功!")
            print(f"MySQL版本: {conn.execute(text('SELECT version()')).scalar()}")
    except Exception as e:
        print(f"❌ 连接失败: {e}")