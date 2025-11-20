
from fastapi import APIRouter
from .core import AutoBuilder

router = APIRouter(prefix="/autobuilder", tags=["autobuilder"])

@router.post("/run")
async def run(parts_dir: str = "parts"):
    ab = AutoBuilder(".")
    return {
        "apply": ab.apply_packs(parts_dir),
        "rebuild": ab.rebuild(),
        "diag": ab.diagnostics(),
        "summary": ab.summary()
    }
