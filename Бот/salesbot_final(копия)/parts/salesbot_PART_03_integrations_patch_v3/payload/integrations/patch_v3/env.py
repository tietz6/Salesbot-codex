
import os
from pathlib import Path

_LOADED=False
def load_env(root: str|None=None):
    global _LOADED
    if _LOADED: return
    rootp = Path(root or ".").resolve()
    for cand in [rootp/".env", rootp/".env.local", Path(".env")]:
        if cand.exists():
            for line in cand.read_text(encoding="utf-8").splitlines():
                line=line.strip()
                if not line or line.startswith("#"): 
                    continue
                if "=" in line:
                    k,v = line.split("=",1)
                    os.environ.setdefault(k.strip(), v.strip())
    _LOADED=True

def get_env(key: str, default: str|None=None):
    return os.getenv(key, default)
