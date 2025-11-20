
import os, base64
from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from .mini_api import MiniAPI

router = APIRouter()
api = MiniAPI()

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    t = request.app.state.mini_templates
    return t.TemplateResponse("index.html", {"request": request, "title": os.getenv("MINI_TITLE","Salesbot Mini WebKit")})

@router.get("/health")
async def health():
    return {"ok": True}

@router.post("/crm/upsert_contact")
async def upsert_contact(phone: str="", email: str="", name: str=""):
    res = api.upsert_contact(phone=phone, email=email, name=name)
    return res

@router.post("/voice/run")
async def voice_run(file: UploadFile = File(...)):
    audio = await file.read()
    result = api.voice_pipeline(audio)
    # cut audio bytes for json
    if result.get("tts_audio_bytes"):
        result["tts_audio_b64"] = base64.b64encode(result["tts_audio_bytes"]).decode("utf-8")
        del result["tts_audio_bytes"]
    return JSONResponse(result)
