
from pathlib import Path

REQUIRED_PATHS = [
    "core/voice_gateway/v1",
    "core/acl/v1",
    "core/router",
    "modules",
    "apps/mini_webkit/v2",
    "integrations/patch_v3"
]

def run(root="."):
    root = Path(root)
    missing=[]
    for p in REQUIRED_PATHS:
        if not (root/p).exists():
            missing.append(p)
    return {"ok": len(missing)==0, "missing": missing}

if __name__ == "__main__":
    print(run())
