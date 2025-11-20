
from fastapi import APIRouter, Request
from .service import CRMSync

router = APIRouter(prefix="/crm_sync/v1", tags=["crm_sync"])
svc = CRMSync()

@router.get("/health")
async def health():
    return {"ok": True, "version": "v1"}

@router.post("/status/{deal_id}")
async def status(deal_id: str, req: Request):
    data = await req.json()
    return svc.sync_status(deal_id, data.get("status"), data.get("reason"))

@router.post("/timeline/{deal_id}")
async def timeline(deal_id: str, req: Request):
    data = await req.json()
    return svc.push_timeline(deal_id, data.get("event","event"), data.get("payload"))

@router.post("/manager/ensure")
async def manager_ensure(req: Request):
    data = await req.json()
    return svc.ensure_manager_profile(data)

@router.post("/bulk_sync")
async def bulk_sync(req: Request):
    data = await req.json()
    return svc.bulk_sync(data.get("deals", []))
