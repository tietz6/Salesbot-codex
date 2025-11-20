
import json, os
from typing import Dict, Any, List
from modules.dialog_memory.v1.service import list_sessions

def aggregate(manager_id: str) -> Dict[str, Any]:
    sessions = list_sessions(manager_id)
    if not sessions:
        return {
            "sessions": [],
            "stats":{
                "total_sessions": 0,
                "avg_score": 0,
                "weak_count": 0,
                "strong_count": 0
            }
        }

    total = len(sessions)
    scores = []
    weak = 0
    strong = 0
    table=[]
    for s in sessions:
        sc = s.get("score")
        if isinstance(sc, (int,float)):
            scores.append(sc)
        weak += len(s.get("errors",[]))
        strong += len(s.get("strengths",[]))
        table.append({
            "session": s.get("session_id"),
            "errors": ", ".join(s.get("errors",[]))[:120],
            "score": sc
        })

    avg = int(sum(scores)/len(scores)) if scores else 0
    return {
        "sessions": sessions,
        "table": table,
        "stats":{
            "total_sessions": total,
            "avg_score": avg,
            "weak_count": weak,
            "strong_count": strong
        }
    }
