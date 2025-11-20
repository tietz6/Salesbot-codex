
import json, urllib.request, urllib.error, os
from .env import get_env
from .retry import retry

DEFAULT_TIMEOUT = float(get_env("HTTP_TIMEOUT", "15"))
DEFAULT_RETRIES = int(get_env("HTTP_RETRIES", "3"))

def _build_headers(headers: dict|None):
    base = {"Content-Type":"application/json"}
    if headers:
        base.update(headers)
    return base

@retry(tries=DEFAULT_RETRIES)
def http_get(url: str, headers: dict|None=None, timeout: float|None=None):
    req = urllib.request.Request(url, method="GET", headers=_build_headers(headers))
    with urllib.request.urlopen(req, timeout=timeout or DEFAULT_TIMEOUT) as r:
        data = r.read().decode("utf-8")
    try:
        return json.loads(data)
    except Exception:
        return data

@retry(tries=DEFAULT_RETRIES)
def http_post(url: str, payload: dict|str|bytes, headers: dict|None=None, timeout: float|None=None):
    if isinstance(payload, dict):
        body = json.dumps(payload).encode("utf-8")
    elif isinstance(payload, str):
        body = payload.encode("utf-8")
    else:
        body = payload
    req = urllib.request.Request(url, data=body, method="POST", headers=_build_headers(headers))
    with urllib.request.urlopen(req, timeout=timeout or DEFAULT_TIMEOUT) as r:
        data = r.read().decode("utf-8")
    try:
        return json.loads(data)
    except Exception:
        return data
