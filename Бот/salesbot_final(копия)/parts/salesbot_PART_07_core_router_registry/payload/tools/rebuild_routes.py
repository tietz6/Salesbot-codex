
import os, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULES = ROOT / "modules"
REGISTRY = ROOT / "core" / "router" / "registry.json"

def collect():
    routes=[]
    for p in MODULES.rglob("routes.py"):
        rel = p.relative_to(ROOT).as_posix()
        routes.append({
            "module": rel,
            "import": rel.replace("/",".")[:-3]
        })
    return routes

def main():
    routes = collect()
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY.write_text(json.dumps({"routes": routes}, indent=2, ensure_ascii=False), encoding="utf-8")
    print("[rebuild_routes] updated", REGISTRY)

if __name__ == "__main__":
    main()
