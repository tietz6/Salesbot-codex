
import os
from typing import Optional, List

from integrations.patch_v3.http_client import http_get, http_post
from integrations.patch_v3.env import get_env
from .auth import CRMAuth
from .schemas import Contact, Deal, Note, to_json
from .errors import CRMError
from .utils import ensure_dict, pick

class CRMClientV4:
    def __init__(self, base_url: Optional[str]=None, token: Optional[str]=None, timeout: Optional[float]=None):
        self.base = (base_url or os.getenv("CRM_API_BASE","")).rstrip("/")
        self.auth = CRMAuth(token=token)
        self.timeout = float(timeout or get_env("CRM_API_TIMEOUT","20"))

    def _url(self, path: str)->str:
        if not self.base:
            raise CRMError("config_error", "CRM_API_BASE is not set")
        return f"{self.base}/{path.lstrip('/')}"

    # ---- Contacts ----
    def get_contact(self, phone: Optional[str]=None, email: Optional[str]=None)->Optional[Contact]:
        params = {}
        if phone: params["phone"]=phone
        if email: params["email"]=email
        res = http_get(self._url("contacts/get"), headers=self.auth.headers(), timeout=self.timeout)
        data = ensure_dict(res).get("contact")
        if not data:
            return None
        return Contact(**data)

    def upsert_contact(self, contact: Contact)->Contact:
        contact = contact.validate()
        payload = {"contact": to_json(contact)}
        res = http_post(self._url("contacts/upsert"), payload, headers=self.auth.headers(), timeout=self.timeout)
        data = ensure_dict(res).get("contact")
        if not data:
            raise CRMError("parse_error", "No 'contact' in response", res)
        return Contact(**data)

    # ---- Deals ----
    def list_deals(self, contact_id: Optional[str]=None)->List[Deal]:
        payload = {"contact_id": contact_id} if contact_id else {}
        res = http_post(self._url("deals/list"), payload, headers=self.auth.headers(), timeout=self.timeout)
        items = ensure_dict(res).get("deals", [])
        return [Deal(**x) for x in items if isinstance(x, dict)]

    def create_deal(self, deal: Deal)->Deal:
        deal = deal.validate()
        payload = {"deal": to_json(deal)}
        res = http_post(self._url("deals/create"), payload, headers=self.auth.headers(), timeout=self.timeout)
        data = ensure_dict(res).get("deal")
        if not data:
            raise CRMError("parse_error", "No 'deal' in response", res)
        return Deal(**data)

    # ---- Notes ----
    def add_note(self, note: Note)->Note:
        note = note.validate()
        payload = {"note": to_json(note)}
        res = http_post(self._url("notes/add"), payload, headers=self.auth.headers(), timeout=self.timeout)
        data = ensure_dict(res).get("note")
        if not data:
            raise CRMError("parse_error", "No 'note' in response", res)
        return Note(**data)
