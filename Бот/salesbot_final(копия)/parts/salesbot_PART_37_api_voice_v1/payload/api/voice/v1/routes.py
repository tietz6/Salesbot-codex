
from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import Response
from core.voice_gateway.v1 import VoicePipeline

router = APIRouter(prefix="/voice/v1", tags=["voice_v1"])
vp = VoicePipeline()

@router.get("/health")
async def health():
    return {"ok": True, "voice_gateway": "v1"}

@router.post("/llm/chat")
async def llm_chat(req: Request):
    data = await req.json()
    messages = data.get("messages", [])
    out = vp.llm.chat(messages or [{"role":"user","content":"Привет"}])
    return {"ok": True, "output": out}

@router.post("/asr/transcribe")
async def asr_transcribe(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    text = vp.asr.transcribe(audio_bytes)
    return {"ok": True, "text": text, "size": len(audio_bytes)}

@router.post("/tts/synth")
async def tts_synth(req: Request):
    data = await req.json()
    text = data.get("text","")
    voice = data.get("voice","neutral")
    audio = vp.tts.synth(text, voice=voice)
    return Response(content=audio, media_type="audio/pcm")
