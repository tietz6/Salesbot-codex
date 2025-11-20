
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from .service import pull_leads, get_lead, push_result, sync_manager_profile, map_to_training, update_lead

router = APIRouter(prefix="/crm_bridge/v2", tags=["crm_bridge"])

CONFIG = {
    "provider": "mock",
    "supports": ["pull","push_result","webhook","profile_sync","map_to_training"]
}

@router.get("/health")
async def health():
    return {"ok": True, "version": "v2"}

@router.get("/config")
async def config():
    return CONFIG

@router.post("/pull_leads")
async def pull(req: Request):
    data = await req.json()
    return {"ok": True, "items": pull_leads(data.get("filters"))}

@router.get("/lead/{lead_id}")
async def lead_get(lead_id: str):
    l = get_lead(lead_id)
    if not l:
        return JSONResponse({"error":"not found"}, status_code=404)
    return l

@router.post("/push_result")
async def push(req: Request):
    data = await req.json()
    out = push_result(
        data.get("lead_id"),
        data.get("manager_id"),
        data.get("result"),
        data.get("transcript"),
        data.get("amount")
    )
    return out

@router.get("/sync_manager/{manager_id}")
async def sync_manager(manager_id: str):
    from .service import sync_manager_profile
    return sync_manager_profile(manager_id)

@router.post("/map_to_training")
async def map_train(req: Request):
    data = await req.json()
    return map_to_training(data.get("lead") or {}, data.get("manager_id","unknown"))

@router.post("/webhook")
async def webhook(req: Request):
    data = await req.json()
    event = data.get("event")
    payload = data.get("payload") or {}
    if event == "lead.update" and payload.get("id"):
        patch = payload.copy(); patch.pop("id", None)
        from .service import update_lead
        lead = update_lead(payload["id"], patch)
        return {"ok": True, "updated": lead}
    return {"ok": True, "received": event}
