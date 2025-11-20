
from dataclasses import asdict
from typing import Optional, Dict, Any

try:
    from products.bundle.v1 import build_bundle
except Exception:
    build_bundle = None

try:
    from bridges.crm_api_bridge.v3 import CRMClient, Contact, Deal
except Exception:
    CRMClient = None
    Contact = None
    Deal = None

try:
    from modules.payments.v1 import PaymentsEngine
except Exception:
    PaymentsEngine = None

class Glue:
    def __init__(self):
        self.crm = CRMClient() if CRMClient else None
        self.pay = PaymentsEngine() if PaymentsEngine else None

    def build_bundle(self, song=True, video=False, premium=False)->dict:
        if not build_bundle:
            return {"ok": False, "error": "products.bundle not available"}
        b = build_bundle(song=song, video=video, premium=premium)
        return {"ok": True, "bundle": b.to_dict()}

    def create_deal(self, title: str, amount: float, currency: str="KGS", contact: Optional[dict]=None)->dict:
        if not self.crm or not Deal or not Contact:
            return {"ok": False, "error": "CRM not available"}

        # upsert contact
        ct_data = contact or {}
        ct = Contact(
            phone=ct_data.get("phone"),
            email=ct_data.get("email"),
            name=ct_data.get("name")
        )
        saved_ct = self.crm.upsert_contact(ct)

        # create deal
        d = Deal(title=title, amount=float(amount), currency=currency, contact_id=saved_ct.id if getattr(saved_ct,'id',None) else None)
        saved_d = self.crm.create_deal(d)

        try:
            return {"ok": True, "deal": asdict(saved_d), "contact": asdict(saved_ct)}
        except Exception:
            return {"ok": True, "deal": {"title": saved_d.title, "amount": saved_d.amount, "currency": saved_d.currency}, "contact": {"phone": saved_ct.phone, "email": saved_ct.email, "name": saved_ct.name}}

    def buy_bundle(self, song=True, video=False, premium=False, contact: Optional[dict]=None)->dict:
        if not self.pay:
            return {"ok": False, "error": "Payments not available"}
        bundle_res = self.build_bundle(song=song, video=video, premium=premium)
        if not bundle_res.get("ok"):
            return bundle_res
        b = bundle_res["bundle"]
        title = b.get("name", "Bundle")
        amount = b.get("base_price", 0.0)
        # create deal first (if CRM available)
        deal_info = None
        if self.crm and Deal:
            d = self.create_deal(title=title, amount=amount, currency=b.get("currency","KGS"), contact=contact)
            deal_info = d.get("deal",{})
        inv = self.pay.create_invoice(amount=amount, currency=b.get("currency","KGS"), deal_id=deal_info.get("id") if isinstance(deal_info, dict) else None)
        return {"ok": True, "bundle": b, "invoice": inv.to_dict(), "deal": deal_info}

    def invoice_status(self, invoice_id: str)->dict:
        if not self.pay:
            return {"ok": False, "error": "Payments not available"}
        inv = self.pay.get_invoice(invoice_id)
        if not inv:
            return {"ok": False, "error": "invoice not found"}
        return {"ok": True, "invoice": inv.to_dict()}
