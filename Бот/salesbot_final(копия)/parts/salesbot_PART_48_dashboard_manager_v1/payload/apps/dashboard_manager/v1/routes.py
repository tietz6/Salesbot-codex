
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, FileResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os, io
import matplotlib.pyplot as plt
from .service import aggregate

router = APIRouter(prefix="/dashboard_manager/v1", tags=["dashboard_manager"])

BASE = os.path.dirname(__file__)
TPL = os.path.join(BASE,"templates")
STATIC = os.path.join(BASE,"static")

env = Environment(
    loader=FileSystemLoader(TPL),
    autoescape=select_autoescape(['html','xml'])
)

@router.get("/static/style.css")
async def css():
    return FileResponse(os.path.join(STATIC,"style.css"))

@router.get("/progress/{manager_id}")
async def progress(manager_id: str):
    data = aggregate(manager_id)
    scores = [s.get("score") for s in data["sessions"] if isinstance(s.get("score"),(int,float))]
    plt.figure(figsize=(6,3))
    if scores:
        plt.plot(scores, linewidth=2)
        plt.ylim(0,100)
    buf=io.BytesIO()
    plt.savefig(buf, format="png", dpi=100, bbox_inches="tight")
    buf.seek(0)
    return FileResponse(buf, media_type="image/png")

@router.get("/{manager_id}", response_class=HTMLResponse)
async def dashboard(manager_id: str):
    data = aggregate(manager_id)
    tpl = env.get_template("dashboard.html")
    html = tpl.render(manager_id=manager_id, **data)
    return HTMLResponse(html)
