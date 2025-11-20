
import json
import subprocess
from pathlib import Path
from tools.rebuild_routes import main as rebuild_routes
from tools.diagnose_startup import run as diagnose
from tools.check_paths import run as check_paths
from tools.check_env import run as check_env

class AutoBuilder:
    def __init__(self, root="."):
        self.root = Path(root).resolve()

    def apply_packs(self, packs_dir: str):
        packs = list(Path(packs_dir).glob("*.zip"))
        packs.sort()
        applied = []

        for pack in packs:
            applied.append(pack.name)
            # Unzip safely
            subprocess.run(["unzip", "-o", str(pack), "-d", self.root], check=False)

        return applied

    def rebuild(self):
        rebuild_routes()
        return True

    def diagnostics(self):
        return {
            "env": check_env(),
            "paths": check_paths(self.root),
            "imports": diagnose()
        }

    def summary(self):
        return {
            "ok": True,
            "message": "AutoBuilder ready"
        }
