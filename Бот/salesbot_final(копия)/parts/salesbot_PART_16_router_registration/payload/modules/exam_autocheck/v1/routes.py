from fastapi import APIRouter
router = APIRouter(prefix="/exam_autocheck", tags=["exam_autocheck"])

@router.get("/health")
async def health():
    return {"ok": True, "module": "exam_autocheck", "version": "v1"}