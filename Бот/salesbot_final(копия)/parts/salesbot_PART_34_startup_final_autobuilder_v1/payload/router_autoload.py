
from fastapi import FastAPI
import importlib

ROUTE_MODULES = [
    # core/public APIs
    "api.voice.v1.routes",
    # modules
    "modules.master_path.v3.routes",
    "modules.objections.v3.routes",
    "modules.upsell.v3.routes",
    "modules.arena.v4.routes",
    "modules.sleeping_dragon.v4.routes",
    "modules.exam_autocheck.v2.routes",
    "modules.payments.v2.routes",
    # apps
    "apps.mini_webkit.v3.routes",
    "apps.public_miniapp.v1.router",
    # bridges
    "bridges.crm_api_bridge.v4.routes",
    "bridges.crm_sync.v1.routes",
    # integrations
    "integrations.patch_v4.routes",
]

def include_all(app: FastAPI)->None:
    attached = []
    errors = []
    for m in ROUTE_MODULES:
        try:
            mod = importlib.import_module(m)
            router = getattr(mod, "router", None)
            if router is None:
                continue
            app.include_router(router)
            attached.append(m)
        except Exception as e:
            errors.append((m, str(e)))

    @app.get("/api/public/v1/routes_summary")
    async def routes_summary():
        return {"attached": attached, "errors": errors}
