
import json, importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = Path(__file__).resolve().parent / "registry.json"

def load_routes():
    if not REGISTRY.exists():
        return []
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    return data.get("routes", [])

def import_all():
    mods = load_routes()
    loaded = []
    for m in mods:
        try:
            modname = m["import"]
            importlib.import_module(modname)
            loaded.append(modname)
        except Exception as e:
            print("[auto_import] FAIL:", m, e)
    return loaded
