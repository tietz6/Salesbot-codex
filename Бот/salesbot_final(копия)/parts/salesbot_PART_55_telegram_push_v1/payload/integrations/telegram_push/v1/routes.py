
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, FileResponse
import os, json
from .service import config, subscribers, update_subscribers, send_push, _load, LOG

router = APIRouter(prefix="/telegram_push/v1", tags=["telegram_push"])

@router.get("/health")
async def health():
    return {"ok": True, "mock_mode": config().get("mock_mode", True)}

@router.get("/subscribers")
async def get_subs():
    return subscribers()

@router.post("/subscribe")
async def subscribe(req: Request):
    data = await req.json()
    manager_id = data.get("manager_id")
    chat_id = data.get("chat_id")
    channels = data.get("channels") or ["training","kpi","cases","deals"]
    if not manager_id or not chat_id:
        return JSONResponse({"error":"manager_id and chat_id required"}, status_code=400)
    m = subscribers()
    m[manager_id] = {"chat_id": str(chat_id), "channels": channels}
    update_subscribers(m)
    return {"ok": True, "manager_id": manager_id}

@router.post("/send")
async def send(req: Request):
    data = await req.json()
    return send_push(
        data.get("manager_id"),
        data.get("channel","training"),
        data.get("template","training.reminder"),
        data.get("payload") or {}
    )

@router.get("/log")
async def log():
    # Return last 200 entries for quick debugging
    try:
        lines = open(LOG, "r", encoding="utf-8").read().strip().splitlines()[-200:]
        return {"ok": True, "items": [json.loads(x) for x in lines if x.strip()]}
    except Exception:
        return {"ok": True, "items": []}

# Helpers for common events
@router.post("/events/training_reminder")
async def ev_training(req: Request):
    data = await req.json()
    return send_push(data.get("manager_id"), "training", "training.reminder", {
        "when": data.get("when","сегодня"),
        "mode": data.get("mode","Arena")
    })

@router.post("/events/percent_up")
async def ev_percent_up(req: Request):
    data = await req.json()
    return send_push(data.get("manager_id"), "kpi", "kpi.percent_up", {"percent": data.get("percent")})

@router.post("/events/to_next")
async def ev_to_next(req: Request):
    data = await req.json()
    return send_push(data.get("manager_id"), "kpi", "kpi.to_next", {
        "remain": data.get("remain",0),
        "next_percent": data.get("next_percent", "—")
    })

@router.post("/events/deal_won")
async def ev_deal_won(req: Request):
    data = await req.json()
    return send_push(data.get("manager_id"), "deals", "deals.won", {
        "id": data.get("id"),
        "amount": data.get("amount",0),
        "income": data.get("income",0)
    })

@router.post("/events/deal_lost")
async def ev_deal_lost(req: Request):
    data = await req.json()
    return send_push(data.get("manager_id"), "deals", "deals.lost", {
        "id": data.get("id"),
        "manager_id": data.get("manager_id")
    })
