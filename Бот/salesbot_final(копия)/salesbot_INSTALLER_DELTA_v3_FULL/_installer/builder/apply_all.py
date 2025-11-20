import os, sys, zipfile

def apply_all(parts_dir: str, target_dir: str):
    zips = sorted([z for z in os.listdir(parts_dir) if z.lower().endswith('.zip')])
    print(f'[autobuilder] Found {len(zips)} archives in {parts_dir}')
    for name in zips:
        path = os.path.join(parts_dir, name)
        print(f'[autobuilder] Applying: {name}')
        with zipfile.ZipFile(path, 'r') as zf:
            zf.extractall(target_dir)
    print('[autobuilder] All parts applied.')

if __name__ == '__main__':
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    parts = os.path.join(root, 'parts')
    if not os.path.isdir(parts):
        print(f'[autobuilder] ERROR: parts/ not found at {parts}')
        sys.exit(1)
    apply_all(parts, root)
