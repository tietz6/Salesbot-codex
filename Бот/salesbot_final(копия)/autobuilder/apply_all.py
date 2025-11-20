
from .core import AutoBuilder
import sys, json, os
def main():
    root = "."
    parts = sys.argv[1] if len(sys.argv)>1 else "parts"
    ab = AutoBuilder(root)
    res = {
        "apply": ab.apply_packs(parts),
        "rebuild": ab.rebuild(),
        "diag": ab.diagnostics(),
        "summary": ab.summary()
    }
    print(json.dumps(res, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
