
import base64
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
try:
    from core.voice_gateway.v1 import VoicePipeline
except Exception as e:
    VoicePipeline = None

router = APIRouter(prefix="/api/voice/v1", tags=["voice"])
_vp = VoicePipeline() if VoicePipeline else None

@router.get("/health")
async def health():
    return {"ok": True, "pipeline": bool(_vp)}

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    if not _vp:
        raise HTTPException(status_code=503, detail="VoicePipeline not available")
    audio = await file.read()
    text = _vp.asr.transcribe(audio)
    return {"ok": True, "text": text}

@router.post("/speak")
async def speak(text: str):
    if not _vp:
        raise HTTPException(status_code=503, detail="VoicePipeline not available")
    audio = _vp.tts.synthesize(text)
    b64 = base64.b64encode(audio).decode("utf-8") if audio else ""
    return JSONResponse({"ok": True, "tts_audio_b64": b64})

@router.post("/ask_llm")
async def ask_llm(text: str, system_prompt: str = "You are a helpful sales coach."):
    if not _vp:
        raise HTTPException(status_code=503, detail="VoicePipeline not available")
    reply = _vp.llm.chat([
        {"role":"system","content":system_prompt},
        {"role":"user","content": text}
    ])
    return {"ok": True, "reply": reply}

@router.post("/run")
async def run(file: UploadFile = File(...), system_prompt: str = "You are a helpful sales coach."):
    if not _vp:
        raise HTTPException(status_code=503, detail="VoicePipeline not available")
    audio = await file.read()
    result = _vp.run(audio, system_prompt=system_prompt)
    if result.get("tts_audio_bytes"):
        result["tts_audio_b64"] = base64.b64encode(result["tts_audio_bytes"]).decode("utf-8")
        del result["tts_audio_bytes"]
    return JSONResponse({"ok": True, **result})
