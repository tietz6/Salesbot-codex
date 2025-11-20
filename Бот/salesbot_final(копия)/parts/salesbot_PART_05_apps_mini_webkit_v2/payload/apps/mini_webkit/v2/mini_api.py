
from typing import Optional
from dataclasses import asdict
try:
    from bridges.crm_api_bridge.v3 import CRMClient, Contact
except Exception:
    CRMClient = None
    Contact = None
try:
    from core.voice_gateway.v1 import VoicePipeline
except Exception:
    VoicePipeline = None

class MiniAPI:
    def __init__(self):
        self.crm = CRMClient() if CRMClient else None
        self.voice = VoicePipeline() if VoicePipeline else None

    def upsert_contact(self, phone: str="", email: str="", name: str="")->dict:
        if not self.crm or not Contact:
            return {"ok": False, "error": "CRM bridge not available"}
        ct = Contact(phone=phone or None, email=email or None, name=name or None)
        saved = self.crm.upsert_contact(ct)
        try:
            return {"ok": True, "contact": asdict(saved)}
        except Exception:
            return {"ok": True, "contact": {"phone": saved.phone, "email": saved.email, "name": saved.name}}

    def voice_pipeline(self, audio_bytes: bytes)->dict:
        if not self.voice:
            return {"ok": False, "error": "Voice pipeline not available"}
        res = self.voice.run(audio_bytes)
        return {"ok": True, **res}
