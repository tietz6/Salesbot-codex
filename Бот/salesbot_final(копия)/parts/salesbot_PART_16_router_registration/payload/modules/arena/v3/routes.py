from fastapi import APIRouter
router = APIRouter(prefix="/arena", tags=["arena"])

@router.get("/health")
async def health():
    return {"ok": True, "module": "arena", "version": "v3"}