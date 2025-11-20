
import os
from fastapi import FastAPI
from tools.rebuild_routes import main as rebuild_routes
from core.router.auto_import import import_all

def create_app():
    # rebuild and import all routes
    rebuild_routes()
    import_all()

    app = FastAPI(
        title="salesbot",
        version="1.0",
        description="Unified Salesbot Application"
    )

    # Mini WebKit (if installed)
    try:
        from apps.mini_webkit.v2 import build_app as build_mini
        build_mini(app)
    except Exception as e:
        print("[startup] mini_webkit skipped:", e)

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("startup:app", host="0.0.0.0", port=int(os.getenv("PORT","8080")), reload=False)
