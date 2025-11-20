
import importlib
from .modules_map import MODULES_MAP

def try_include(app):
    loaded = {}
    for key, cfg in MODULES_MAP.items():
        targets = [cfg.get("preferred")] + list(cfg.get("fallbacks", []))
        for target in targets:
            if not target:
                continue
            try:
                mod = importlib.import_module(target)
                if hasattr(mod, "router"):
                    app.include_router(mod.router)
                    loaded[key] = target
                    break
            except Exception:
                continue
    return loaded
