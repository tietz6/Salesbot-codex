
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os, json, datetime

router = APIRouter(prefix="/mini/brand", tags=["mini_brand"])

BASE_DIR = os.path.dirname(__file__)
TPL_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")
THEME_PATH = os.path.join(BASE_DIR, "theme.json")

env = Environment(
    loader=FileSystemLoader(TPL_DIR),
    autoescape=select_autoescape(['html', 'xml'])
)

def theme():
    try:
        with open(THEME_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"brand":"На Счастье"}

@router.get("/static/brand.css")
async def css():
    return FileResponse(os.path.join(STATIC_DIR, "brand.css"))

@router.get("/health")
async def health():
    return {"ok": True, "brand": theme().get("brand"), "version": "v1"}

@router.get("/hub", response_class=HTMLResponse)
async def hub():
    t = env.get_template("hub.html")
    html = t.render(title="На Счастье · Хаб", year=datetime.datetime.now().year,
                    stats={"sessions": 128, "avg_score": 82, "objections_closed": 314, "upsells": 57})
    return HTMLResponse(html)

@router.get("/rubric", response_class=HTMLResponse)
async def rubric():
    # ленивый линк на API рубрик
    return HTMLResponse(f"""
      <html><head><link rel='stylesheet' href='/mini/brand/static/brand.css'></head>
      <body class='container'><h3>Рубрика «Путь Мастера»</h3>
      <p><a class='link' href='/master_path_rubrics/v1/rubric' target='_blank'>Открыть JSON рубрики</a></p>
      <p><a class='link' href='/mini/brand/hub'>← Назад в хаб</a></p>
      </body></html>
    """)

@router.get("/arena/info", response_class=HTMLResponse)
async def arena_info():
    return HTMLResponse("""
      <html><head><link rel='stylesheet' href='/mini/brand/static/brand.css'></head>
      <body class='container'><h3>Арена</h3>
      <p>8 психотипов, динамика эмоций, уровни сложности и штрафы за слабые ответы.</p>
      <p><a class='link' href='/mini/brand/hub'>← Назад в хаб</a></p>
      </body></html>
    """)

@router.get("/obj/info", response_class=HTMLResponse)
async def obj_info():
    return HTMLResponse("""
      <html><head><link rel='stylesheet' href='/mini/brand/static/brand.css'></head>
      <body class='container'><h3>Возражения</h3>
      <p>Классификатор + матрица подсказок + штрафная модель 0..10</p>
      <p><a class='link' href='/mini/brand/hub'>← Назад в хаб</a></p>
      </body></html>
    """)

@router.get("/upsell/info", response_class=HTMLResponse)
async def upsell_info():
    return HTMLResponse("""
      <html><head><link rel='stylesheet' href='/mini/brand/static/brand.css'></head>
      <body class='container'><h3>Доп. продажи</h3>
      <p>Подсчёт цены/скидки/купона/НДС + аргументация выгоды.</p>
      <p><a class='link' href='/mini/brand/hub'>← Назад в хаб</a></p>
      </body></html>
    """)

# Быстрые переходы (заглушки-линки на существующие API)
@router.get("/go/master")
async def go_master():
    return JSONResponse({"open": "/master_path/v3/start/test"})

@router.get("/go/arena")
async def go_arena():
    return JSONResponse({"open": "/arena_psy/v1/spawn"})

@router.get("/go/obj")
async def go_obj():
    return JSONResponse({"open": "/objections_classifier/v1/classify"})

@router.get("/go/upsell")
async def go_upsell():
    return JSONResponse({"open": "/upsell_pricing/v1/compute"})
