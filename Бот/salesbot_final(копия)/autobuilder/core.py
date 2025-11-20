
import os, json, zipfile, shutil
from pathlib import Path
from typing import List, Dict

class AutoBuilder:
    def __init__(self, project_root: str|Path):
        self.root = Path(project_root)

    def apply_pack(self, zip_path: str|Path)->dict:
        zip_path = Path(zip_path)
        with zipfile.ZipFile(zip_path, 'r') as z:
            # read manifest inside zip
            manifest_data = None
            for name in z.namelist():
                if name.endswith("manifest.json"):
                    manifest_data = json.loads(z.read(name).decode("utf-8"))
                    break
            if not manifest_data:
                return {"ok": False, "error": "manifest.json not found"}

            ops = manifest_data.get("operations", [])
            # extract to temp
            tmp = self.root/".ab_tmp"
            if tmp.exists(): shutil.rmtree(tmp)
            tmp.mkdir(parents=True, exist_ok=True)
            z.extractall(tmp)

            # find payload dir
            payload_dir = None
            for p in tmp.rglob("payload"):
                if p.is_dir():
                    payload_dir = p
                    break
            if not payload_dir:
                return {"ok": False, "error": "payload dir missing"}

            for op in ops:
                src = (payload_dir / op["src"].split("payload/")[-1]) if op["src"].startswith("payload/") else (tmp/op["src"])
                dst = self.root / op["dst"]
                if op["op"] == "REPLACE":
                    if dst.exists():
                        shutil.rmtree(dst) if dst.is_dir() else dst.unlink()
                    if src.is_dir():
                        shutil.copytree(src, dst)
                    else:
                        dst.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src, dst)
                elif op["op"] == "ADD_ONLY":
                    if not dst.exists():
                        if src.is_dir():
                            shutil.copytree(src, dst)
                        else:
                            dst.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(src, dst)
                else:
                    return {"ok": False, "error": f"unknown op {op['op']}"}

            shutil.rmtree(tmp, ignore_errors=True)
            return {"ok": True, "pack": zip_path.name, "ops": len(ops)}

    def apply_packs(self, parts_dir: str|Path)->list:
        parts = []
        for p in sorted(Path(parts_dir).glob("*.zip")):
            parts.append(self.apply_pack(p))
        return parts

    def rebuild(self)->dict:
        # placeholder for future static builds, migrations, etc.
        return {"ok": True, "rebuild": "noop"}

    def diagnostics(self)->dict:
        # quick checks for required files
        needed = ["startup.py", "router_autoload.py"]
        missing = [n for n in needed if not (self.root/n).exists()]
        return {"ok": True, "missing": missing}

    def summary(self)->dict:
        return {"ok": True, "root": str(self.root)}
