
import importlib, json
from pathlib import Path

def check_registry():
    reg = Path("core/router/registry.json")
    if not reg.exists():
        return {"ok": False, "error": "registry.json missing"}
    try:
        data = json.loads(reg.read_text(encoding="utf-8"))
        return {"ok": True, "routes": len(data.get("routes",[]))}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def check_imports():
    reg = Path("core/router/registry.json")
    if not reg.exists():
        return {"ok": False, "error": "no registry"}
    data = json.loads(reg.read_text())
    fails=[]
    for r in data.get("routes",[]):
        try:
            importlib.import_module(r["import"])
        except Exception as e:
            fails.append({"module":r["import"],"error":str(e)})
    return {"ok": len(fails)==0, "fails": fails}

def run():
    a = check_registry()
    b = check_imports()
    return {"registry": a, "imports": b}

if __name__ == "__main__":
    print(run())
