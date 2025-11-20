
from fastapi import APIRouter, Request
from .renderer import MiniRenderer

router = APIRouter(prefix="/mini/v3", tags=["mini_webkit"])
r = MiniRenderer()

@router.get("/health")
async def health():
    return {"ok": True, "version": "v3"}

@router.get("/version")
async def version():
    return {"ok": True, "mini_webkit": "v3"}

@router.post("/preview/bundle")
async def preview_bundle(request: Request):
    data = await request.json()
    html = r.bundle(data)
    return html

@router.post("/preview/dialog")
async def preview_dialog(request: Request):
    data = await request.json()
    html = r.dialog(data.get("history", []))
    return html

@router.post("/preview/exam")
async def preview_exam(request: Request):
    data = await request.json()
    html = r.exam(data)
    return html
