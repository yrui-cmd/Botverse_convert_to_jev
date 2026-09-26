#!/usr/bin/env python3
import argparse, json, subprocess, sys, tempfile
from pathlib import Path

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('baseline_json')
    ap.add_argument('source_skill_path')
    args = ap.parse_args()
    base = json.loads(Path(args.baseline_json).read_text(encoding='utf-8'))
    helper = Path(__file__).with_name('snapshot_skill.py')
    p = subprocess.run([sys.executable, str(helper), args.source_skill_path], capture_output=True, text=True)
    if p.returncode:
        print(p.stderr, file=sys.stderr)
        raise SystemExit(p.returncode)
    now = json.loads(p.stdout)
    before = base.get('snapshot', base.get('source', {}).get('snapshot', {}))
    after = now['snapshot']
    if before == after:
        print(json.dumps({'unchanged': True, 'changed': [], 'added': [], 'removed': []}, indent=2))
        raise SystemExit(0)
    b, a = set(before), set(after)
    changed = sorted(k for k in b & a if before[k] != after[k])
    added = sorted(a - b)
    removed = sorted(b - a)
    print(json.dumps({'unchanged': False, 'changed': changed, 'added': added, 'removed': removed}, indent=2))
    raise SystemExit(2)
