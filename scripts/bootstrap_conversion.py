#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

IGNORED = {".git", "__pycache__", ".pytest_cache"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def snapshot(root: Path) -> dict[str, dict[str, object]]:
    files: dict[str, dict[str, object]] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in IGNORED for part in path.parts):
            continue
        files[path.relative_to(root).as_posix()] = {
            "sha256": sha256(path),
            "bytes": path.stat().st_size,
        }
    return files


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create an additive Jev conversion workspace from an existing Skill."
    )
    parser.add_argument("source_skill_path")
    parser.add_argument("--output-parent")
    parser.add_argument("--output-name")
    args = parser.parse_args()

    source = Path(args.source_skill_path).expanduser().resolve(strict=True)
    if not source.is_dir() or not (source / "SKILL.md").is_file():
        raise SystemExit("source_skill_path must contain SKILL.md")

    parent = (
        Path(args.output_parent).expanduser().resolve()
        if args.output_parent
        else source.parent
    )
    output_name = args.output_name or f"{source.name}-jev"
    if not output_name or Path(output_name).name != output_name or output_name in {".", ".."}:
        raise SystemExit("output name must be a single directory name")

    destination = (parent / output_name).resolve()
    if destination == source or destination.is_relative_to(source):
        raise SystemExit("destination must be separate from source")
    if destination.exists():
        raise SystemExit(f"destination already exists: {destination}")

    baseline = snapshot(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache"),
    )
    manifest = {
        "source": {"path": str(source), "snapshot": baseline},
        "destination": {"path": str(destination)},
        "status": "IN_PROGRESS",
        "checks": {
            "source_and_destination_distinct": True,
            "source_skill_present": True,
        },
        "repairs": [],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    (destination / "conversion_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "ok": True,
        "source": str(source),
        "destination": str(destination),
        "files_snapshotted": len(baseline),
        "status": "IN_PROGRESS",
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
