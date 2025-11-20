
import os, json, time, statistics
from typing import List, Dict, Any, Optional

LEADS_PATH = os.path.join(os.path.dirname(__file__), "data", "leads.json")

def _load_leads()->List[dict]:
    if not os.path.exists(LEADS_PATH):
        return []
    with open(LEADS_PATH,"r",encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []

def _save_leads(items: List[dict]):
    with open(LEADS_PATH,"w",encoding="utf-8") as f:
        json.dump(items,f,ensure_ascii=False,indent=2)

def pull_leads(filters: Optional[dict]=None)->List[dict]:
    items = _load_leads()
    if not filters:
        return items
    out=[]
    for x in items:
        ok=True
        for k,v in filters.items():
            if v is None: 
                continue
            if k not in x: 
                continue
            if str(x[k]) != str(v):
                ok=False; break
        if ok: out.append(x)
    return out

def get_lead(lead_id: str)->Optional[dict]:
    for x in _load_leads():
        if x.get("id")==lead_id:
            return x
    return None

def update_lead(lead_id: str, patch: dict)->Optional[dict]:
    items = _load_leads()
    for i,x in enumerate(items):
        if x.get("id")==lead_id:
            x.update(patch or {})
            items[i]=x
            _save_leads(items)
            return x
    return None

def push_result(lead_id: str, manager_id: str, result: str, transcript: Optional[str], amount: Optional[float])->dict:
    # result: won/lost/pending
    lead = get_lead(lead_id)
    if not lead:
        return {"ok": False, "error":"lead not found"}
    patch = {"status": result, "assigned_to": manager_id, "closed_at": time.time()}
    if amount is not None:
        patch["amount_final"] = float(amount)
    if transcript:
        patch["transcript"] = transcript
    lead = update_lead(lead_id, patch)
    # simple score from dialog_memory if available
    try:
        from modules.dialog_memory.v1.service import list_sessions
        sessions = list_sessions(manager_id)
        scores = [s.get("score") for s in sessions if isinstance(s.get("score"), (int,float))]
        avg = int(statistics.mean(scores)) if scores else 0
    except Exception:
        avg = 0
    return {"ok": True, "lead": lead, "manager_avg_score": avg}

def sync_manager_profile(manager_id: str)->dict:
    # aggregate dialog memory + suggested lessons
    profile = {"manager_id": manager_id, "avg_score": 0, "last_errors": [], "recommend_lessons": []}
    try:
        from modules.dialog_memory.v1.service import list_sessions
        sessions = list_sessions(manager_id)
        sc = [s.get("score") for s in sessions if isinstance(s.get("score"), (int,float))]
        profile["avg_score"] = int(statistics.mean(sc)) if sc else 0
        errs = []
        for s in sorted(sessions, key=lambda x: x.get("timestamp",0), reverse=True)[:3]:
            errs.extend(s.get("errors",[]))
        profile["last_errors"] = errs[:5]
    except Exception:
        pass
    try:
        from modules.edu_lessons.v1.service import recommend_lessons
        profile["recommend_lessons"] = recommend_lessons(manager_id)
    except Exception:
        profile["recommend_lessons"] = []
    return profile

def map_to_training(lead: dict, manager_id: str)->dict:
    # heuristic mapping from lead data to training modules
    rec = []
    goal = (lead.get("goal") or "").lower()
    budget = (lead.get("budget") or "").lower()
    notes = (lead.get("notes") or "").lower()
    if "дорог" in notes or budget == "low":
        rec.append("objections/price")
    if "довер" in notes:
        rec.append("objections/trust")
    if goal in ["anniversary","romance","family"]:
        rec.append("master_path/offer")
    if goal in ["corporate"]:
        rec.append("upsell/value")
    # fallback
    if not rec:
        rec = ["master_path/qualification"]
    # add memory-based top advice
    prof = sync_manager_profile(manager_id)
    return {"recommend": list(dict.fromkeys(rec + prof.get('recommend_lessons',[])[:2]))}

