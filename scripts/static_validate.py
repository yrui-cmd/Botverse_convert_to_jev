#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path

SECRET_PATTERNS = [
    re.compile(r'(?i)(api[_-]?key|secret|token)\s*[:=]\s*["\']?[A-Za-z0-9_\-]{20,}'),
]

def validate(root: Path):
    failures = []
    required = [root / 'SKILL.md']
    for p in required:
        if not p.exists(): failures.append(f'missing:{p.name}')
    for p in root.rglob('*.json'):
        try: json.loads(p.read_text(encoding='utf-8'))
        except Exception as e: failures.append(f'invalid_json:{p.relative_to(root)}:{e}')
    for p in root.rglob('*'):
        if not p.is_file() or p.stat().st_size > 2_000_000: continue
        try: text = p.read_text(encoding='utf-8')
        except Exception: continue
        for pat in SECRET_PATTERNS:
            if pat.search(text):
                failures.append(f'possible_secret:{p.relative_to(root)}')
        if re.search(r'while\s+true|while\s*\(\s*true\s*\)', text, re.I) and 'max_' not in text.lower():
            failures.append(f'possible_unbounded_loop:{p.relative_to(root)}')
    return failures

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('converted_skill_path')
    args = ap.parse_args()
    root = Path(args.converted_skill_path).resolve()
    failures = validate(root)
    print(json.dumps({'pass': not failures, 'failures': failures}, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not failures else 1)
