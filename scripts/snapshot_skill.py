#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path

IGNORE = {'.git', '__pycache__'}

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def snapshot(root: Path):
    out = {}
    for p in sorted(root.rglob('*')):
        if not p.is_file() or any(part in IGNORE for part in p.parts):
            continue
        out[str(p.relative_to(root)).replace('\\', '/')] = {
            'sha256': digest(p),
            'bytes': p.stat().st_size
        }
    return out

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('skill_path')
    ap.add_argument('-o', '--output')
    args = ap.parse_args()
    root = Path(args.skill_path).resolve()
    if not root.is_dir():
        raise SystemExit(f'Not a directory: {root}')
    data = {'path': str(root), 'snapshot': snapshot(root)}
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(text, encoding='utf-8')
    else:
        print(text)
