from fastapi import APIRouter,Depends
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import text

from backend.app.utils.database import get_db

router = APIRouter(tags=["DB test"])

@router.get("/test-db")
async def test_db(db : Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        return {"status": "success", "result": str(result)}
    except Exception as e:
        return {"status": "failed", "error": str(e)}
