
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from .routes import router as mini_router

def build_app(app: FastAPI|None=None)->FastAPI:
    app = app or FastAPI(title=os.getenv("MINI_TITLE","Salesbot Mini WebKit"))
    # Mount templates/static
    templates = Jinja2Templates(directory=str((__file__[:-7] + "templates").replace("__init__.py","")))
    # expose templates instance on app state
    app.state.mini_templates = templates

    static_dir = __file__[:-7] + "static"
    app.mount("/mini/static", StaticFiles(directory=static_dir), name="mini_static")

    # Router
    app.include_router(mini_router, prefix="/mini")
    return app
