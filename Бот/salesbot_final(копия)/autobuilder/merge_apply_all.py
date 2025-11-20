# autobuilder/merge_apply_all.py
import shutil
from pathlib import Path
import zipfile
import json

ROOT = Path(__file__).resolve().parents[1]           # salesbot_final/
PARTS = ROOT / "parts"
API_MODULES = ROOT / "api" / "modules"

def unzip_all_parts():
    if not PARTS.exists():
        print(f"[parts] dir not found: {PARTS}")
        return
    for z in PARTS.glob("*.zip"):
        dest = PARTS / z.stem
        if dest.exists():
            continue
        print(f"[unzip] {z.name} -> {dest.name}")
        with zipfile.ZipFile(z, "r") as zf:
            zf.extractall(dest)

def iter_payload_module_dirs():
    """Find all .../payload/modules/<module>/<version> inside parts."""
    for part in PARTS.iterdir():
        if not part.is_dir():
            continue
        payload = part / "payload" / "modules"
        if not payload.exists():
            continue
        for mod_dir in payload.iterdir():
            if not mod_dir.is_dir():
                continue
            for ver_dir in mod_dir.iterdir():
                if ver_dir.is_dir():
                    yield (mod_dir.name, ver_dir.name, ver_dir)

def safe_copytree(src: Path, dst: Path):
    dst.mkdir(parents=True, exist_ok=True)
    for p in src.rglob("*"):
        rel = p.relative_to(src)
        out = dst / rel
        if p.is_dir():
            out.mkdir(parents=True, exist_ok=True)
        else:
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, out)

def semantic_sort(versions):
    def key(v):
        try:
            return int(v.lstrip("v"))
        except:
            return 10**9
    return sorted(versions, key=key)

def read_manifest(part_dir: Path):
    m = part_dir / "manifest.json"
    if m.exists():
        try:
            return json.loads(m.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[warn] bad manifest at {m}: {e}")
    return {}

def apply_parts_merge():
    API_MODULES.mkdir(parents=True, exist_ok=True)

    modules_map = {}  # { 'upsell': {'v1':[paths...], 'v3':[paths...]}, ... }
    for module_name, version, ver_path in iter_payload_module_dirs():
        modules_map.setdefault(module_name, {}).setdefault(version, []).append(ver_path)

    if not modules_map:
        print("[apply] nothing found under parts/*/payload/modules/*")
        return

    for module_name, versions in modules_map.items():
        target_base = API_MODULES / module_name
        current_dir = target_base / "_current"
        if current_dir.exists():
            shutil.rmtree(current_dir)
        current_dir.mkdir(parents=True, exist_ok=True)

        ordered = semantic_sort(list(versions.keys()))
        print(f"[merge] {module_name}: {' -> '.join(ordered)} -> _current" )

        for v in ordered:
            for src in versions[v]:
                safe_copytree(src, current_dir)

        for v in versions:
            out_v = target_base / v
            if not out_v.exists():
                safe_copytree(versions[v][0], out_v)

    print("[apply] done. modules merged to api/modules/<name>/_current")

if __name__ == "__main__":
    unzip_all_parts()
    apply_parts_merge()
