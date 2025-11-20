
import json, time
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from core.state.v1 import StateStore
from bridges.crm_api_bridge.v4 import CRMClient, Deal, Note, Contact, CRMError

STATUS_MAP = {
    "new":"new",
    "in_progress":"in_progress",
    "waiting_payment":"waiting_payment",
    "paid":"won",
    "failed":"lost",
    "lost":"lost",
    "won":"won",
}

@dataclass
class ManagerProfile:
    id: str
    name: Optional[str]=None
    phone: Optional[str]=None
    email: Optional[str]=None

class CRMSync:
    def __init__(self):
        self.cache = StateStore("salesbot.db")  # kv cache
        self.crm = CRMClient()

    # ---- status sync ----
    def sync_status(self, deal_id: str, status: str, reason: Optional[str]=None)->dict:
        status = STATUS_MAP.get(status, "in_progress")
        # fetch existing: (optional list or get by id depending on CRM)
        try:
            # We don't have get_deal, so we push via create/update endpoint pattern
            d = Deal(id=deal_id, status=status).validate()
            saved = self.crm.create_deal(d)  # assuming upsert semantics on backend
        except CRMError as e:
            return {"ok": False, "error": e.to_dict()}

        # timeline note
        try:
            text = f"[status] → {status}"
            if reason:
                text += f" | reason: {reason}"
            note = Note(deal_id=deal_id, text=text).validate()
            _ = self.crm.add_note(note)
        except CRMError as e:
            # still ok but with warning
            return {"ok": True, "deal_id": deal_id, "status": status, "warning": e.to_dict()}

        return {"ok": True, "deal_id": deal_id, "status": status}

    # ---- timeline ----
    def push_timeline(self, deal_id: str, event: str, payload: Optional[dict]=None)->dict:
        try:
            text = f"[event] {event}"
            if payload:
                text += f" | {json.dumps(payload, ensure_ascii=False)[:400]}"
            note = Note(deal_id=deal_id, text=text).validate()
            _ = self.crm.add_note(note)
            return {"ok": True}
        except CRMError as e:
            return {"ok": False, "error": e.to_dict()}

    # ---- manager profile ----
    def ensure_manager_profile(self, mgr: dict)->dict:
        mp = ManagerProfile(**mgr)
        # store in kv for now
        key = f"mgr:{mp.id}"
        self.cache.set(key, json.dumps(asdict(mp), ensure_ascii=False))
        # optional: also sync to CRM contacts
        try:
            if mp.phone or mp.email:
                ct = Contact(phone=mp.phone, email=mp.email, name=mp.name).validate()
                saved = self.crm.upsert_contact(ct)
                return {"ok": True, "kv": key, "contact_id": getattr(saved, "id", None)}
            return {"ok": True, "kv": key}
        except CRMError as e:
            return {"ok": True, "kv": key, "warning": e.to_dict()}

    # ---- bulk sync ----
    def bulk_sync(self, deals: List[dict])->dict:
        results = []
        for d in deals or []:
            rid = d.get("id")
            st = d.get("status","in_progress")
            try:
                res = self.sync_status(rid, st)
                results.append({"id": rid, **res})
            except Exception as e:
                results.append({"id": rid, "ok": False, "error": str(e)})
        return {"ok": True, "results": results}
