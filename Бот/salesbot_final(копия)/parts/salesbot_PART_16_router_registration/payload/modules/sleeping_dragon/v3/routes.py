from fastapi import APIRouter
router = APIRouter(prefix="/sleeping_dragon", tags=["sleeping_dragon"])

@router.get("/health")
async def health():
    return {"ok": True, "module": "sleeping_dragon", "version": "v3"}