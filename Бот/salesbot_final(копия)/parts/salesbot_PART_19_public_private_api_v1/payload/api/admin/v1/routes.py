
from fastapi import APIRouter
import sqlite3

router = APIRouter(prefix="/api/admin/v1", tags=["admin-api"])

@router.get("/db_keys")
async def db_keys():
    out=[]
    try:
        conn = sqlite3.connect("salesbot.db")
        cur = conn.execute("SELECT k FROM kv LIMIT 100")
        out=[r[0] for r in cur.fetchall()]
        conn.close()
    except Exception as e:
        return {"ok": False, "error": str(e)}
    return {"ok": True, "keys": out}

@router.get("/stats")
async def stats():
    return {
        "ok": True,
        "modules": {
            "public_api": "v1",
            "admin_api": "v1"
        }
    }
