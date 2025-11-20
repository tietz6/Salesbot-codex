
import importlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "core" / "router" / "registry.json"

def main():
    if not REGISTRY.exists():
        print("[smoke] registry not found")
        return 0
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    ok=True
    for r in reg.get("routes",[]):
        try:
            importlib.import_module(r["import"])
        except Exception as e:
            print("[smoke][FAIL]", r, e)
            ok=False
    if ok:
        print("[smoke] OK")
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
