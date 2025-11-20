
import os
from typing import List, Optional
from .auth import CRMAuth
from .schemas import Contact, Deal, Note, to_json
from integrations.patch_v3.http_client import http_get, http_post
from integrations.patch_v3.env import get_env

class CRMClient:
    def __init__(self, base_url: str|None=None, auth: CRMAuth|None=None, timeout: float|None=None):
        self.base = (base_url or os.getenv("CRM_API_BASE","")).rstrip("/")
        self.auth = auth or CRMAuth()
        self.timeout = float(timeout or get_env("CRM_API_TIMEOUT","20"))

    def _url(self, path: str)->str:
        return f"{self.base}/{path.lstrip('/')}"

    def get_contact(self, phone: str|None=None, email: str|None=None)->Optional[Contact]:
        params = {}
        if phone: params["phone"]=phone
        if email: params["email"]=email
        res = http_get(self._url("contacts/get"), headers=self.auth.headers(), timeout=self.timeout)
        # demo: assume API returns JSON with 'contact'
        data = res.get("contact") if isinstance(res, dict) else None
        if not data: return None
        return Contact(**data)

    def upsert_contact(self, contact: Contact)->Contact:
        payload = {"contact": to_json(contact)}
        res = http_post(self._url("contacts/upsert"), payload, headers=self.auth.headers(), timeout=self.timeout)
        data = res.get("contact") if isinstance(res, dict) else None
        return Contact(**data) if data else contact

    def list_deals(self, contact_id: str|None=None)->List[Deal]:
        payload = {"contact_id": contact_id} if contact_id else {}
        res = http_post(self._url("deals/list"), payload, headers=self.auth.headers(), timeout=self.timeout)
        items = res.get("deals") if isinstance(res, dict) else []
        return [Deal(**x) for x in items]

    def create_deal(self, deal: Deal)->Deal:
        payload = {"deal": to_json(deal)}
        res = http_post(self._url("deals/create"), payload, headers=self.auth.headers(), timeout=self.timeout)
        data = res.get("deal") if isinstance(res, dict) else None
        return Deal(**data) if data else deal

    def add_note(self, note: Note)->Note:
        payload = {"note": to_json(note)}
        res = http_post(self._url("notes/add"), payload, headers=self.auth.headers(), timeout=self.timeout)
        data = res.get("note") if isinstance(res, dict) else None
        return Note(**data) if data else note
