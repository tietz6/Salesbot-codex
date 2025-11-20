
from fastapi import APIRouter
router = APIRouter(prefix="/crm/v4", tags=["crm-v4"])

@router.get("/health")
async def health():
    return {"ok": True, "version": "v4"}
