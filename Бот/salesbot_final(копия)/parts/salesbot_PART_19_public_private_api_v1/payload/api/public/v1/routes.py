
from fastapi import APIRouter
import time, uuid

router = APIRouter(prefix="/api/public/v1", tags=["public-api"])

@router.get("/ping")
async def ping():
    return {"ok": True, "ts": time.time()}

@router.get("/version")
async def version():
    return {"ok": True, "version": "v1", "build": str(uuid.uuid4())}

@router.get("/health")
async def health():
    return {"ok": True, "status": "alive"}
