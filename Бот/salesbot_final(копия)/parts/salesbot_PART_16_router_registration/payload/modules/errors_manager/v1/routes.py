from fastapi import APIRouter
router = APIRouter(prefix="/errors_manager", tags=["errors_manager"])

@router.get("/health")
async def health():
    return {"ok": True, "module": "errors_manager", "version": "v1"}