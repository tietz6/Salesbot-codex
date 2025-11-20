from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pathlib import Path
import os

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", "config", ".env"))
except Exception:
    pass

app = FastAPI(title="SalesBot API (DELTA_v3)", version="3.0.0")

@app.get("/api/public/v1/health")
def health():
    return {"ok": True, "ver": "delta_v3"}

@app.get("/")
def root():
    return JSONResponse({
        "ok": True,
        "message": "SalesBot API (DELTA_v3) поднят.",
        "docs": "http://127.0.0.1:8080/docs",
        "health": "http://127.0.0.1:8080/api/public/v1/health"
    })

def _try_include_dynamic():
    import importlib
    candidates = [
        "api.startup",
        "startup",
        "core.router_registry",
    ]
    for mod in candidates:
        try:
            m = importlib.import_module(mod)
            if hasattr(m, "app"):
                app.mount("/legacy", m.app)
            elif hasattr(m, "get_app"):
                legacy = m.get_app()
                app.mount("/legacy", legacy)
        except Exception:
            pass

_try_include_dynamic()
