
import json, secrets
from fastapi import APIRouter, Request, HTTPException
from core.state.v1 import StateStore

router = APIRouter(prefix="/miniapp/v1", tags=["public_miniapp"])
store = StateStore("salesbot.db")

def _make_key():
    return "miniapp:" + secrets.token_hex(8)

@router.get("/health")
async def health():
    return {"ok": True, "version": "v1"}

@router.post("/create_key")
async def create_key(req: Request):
    data = await req.json()
    key = _make_key()
    store.set(key, json.dumps(data, ensure_ascii=False))
    return {"ok": True, "key": key}

def _load_or_404(key: str):
    raw = store.get(key)
    if not raw:
        raise HTTPException(404, "Key not found")
    try:
        return json.loads(raw)
    except:
        raise HTTPException(500, "Corrupt data")

def _render_iframe(url: str)->str:
    with open(__file__.replace("router.py","templates/open.html"), "r", encoding="utf-8") as f:
        tpl = f.read()
    return tpl.replace("{{URL}}", url)

@router.get("/open/bundle/{key}")
async def open_bundle(key: str):
    data = _load_or_404(key)
    return _render_iframe("/mini/v3/preview/bundle")

@router.get("/open/dialog/{key}")
async def open_dialog(key: str):
    data = _load_or_404(key)
    return _render_iframe("/mini/v3/preview/dialog")

@router.get("/open/exam/{key}")
async def open_exam(key: str):
    data = _load_or_404(key)
    return _render_iframe("/mini/v3/preview/exam")
