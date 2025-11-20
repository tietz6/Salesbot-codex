
from fastapi import FastAPI
from typing import List
import importlib

app = FastAPI(title="salesbot", version="v1-final")

# basic health
@app.get("/api/public/v1/health")
async def root_health():
    return {"ok": True, "app": "salesbot", "version": "v1-final"}

# router autoload
try:
    from router_autoload import include_all
    include_all(app)
except Exception as e:
    @app.get("/api/public/v1/router_error")
    async def router_error():
        return {"ok": False, "error": str(e)}

# optional autobuilder API (can be disabled)
try:
    from autobuilder.routes import router as autobuilder_router
    app.include_router(autobuilder_router)
except Exception:
    pass
