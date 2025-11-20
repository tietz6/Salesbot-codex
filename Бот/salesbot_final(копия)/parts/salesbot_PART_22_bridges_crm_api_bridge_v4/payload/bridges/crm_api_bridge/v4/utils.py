
from typing import Any, Dict

def ensure_dict(x: Any)->Dict:
    if isinstance(x, dict):
        return x
    try:
        import json
        return json.loads(x) if isinstance(x, (bytes,str)) else {}
    except Exception:
        return {}

def pick(data: dict, key: str, default=None):
    if not isinstance(data, dict):
        return default
    return data.get(key, default)
