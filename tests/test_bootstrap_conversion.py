from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = ROOT / "scripts" / "bootstrap_conversion.py"
VERIFY = ROOT / "scripts" / "verify_source_unchanged.py"


class BootstrapConversionTests(unittest.TestCase):
    def test_creates_copy_manifest_and_preserves_source(self):
        with tempfile.TemporaryDirectory() as temporary:
            work = Path(temporary)
            source = work / "sample-skill"
            source.mkdir()
            (source / "SKILL.md").write_text(
                "---\nname: sample-skill\ndescription: test skill\n---\n\n# Sample\n",
                encoding="utf-8",
            )
            (source / "script.py").write_text("print('ok')\n", encoding="utf-8")
            original = {
                path.relative_to(source).as_posix(): path.read_bytes()
                for path in source.rglob("*") if path.is_file()
            }

            created = subprocess.run(
                [sys.executable, str(BOOTSTRAP), str(source), "--output-parent", str(work)],
                check=True,
                capture_output=True,
                text=True,
            )
            report = json.loads(created.stdout)
            destination = Path(report["destination"])
            manifest = destination / "conversion_manifest.json"

            self.assertEqual(destination.name, "sample-skill-jev")
            self.assertTrue(manifest.is_file())
            self.assertEqual(
                json.loads(manifest.read_text(encoding="utf-8"))["status"],
                "IN_PROGRESS",
            )
            self.assertEqual(
                original,
                {
                    path.relative_to(source).as_posix(): path.read_bytes()
                    for path in source.rglob("*") if path.is_file()
                },
            )
            verified = subprocess.run(
                [sys.executable, str(VERIFY), str(manifest), str(source)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(verified.returncode, 0, verified.stdout + verified.stderr)
            self.assertTrue(json.loads(verified.stdout)["unchanged"])

    def test_refuses_existing_destination(self):
        with tempfile.TemporaryDirectory() as temporary:
            work = Path(temporary)
            source = work / "source"
            source.mkdir()
            (source / "SKILL.md").write_text("---\nname: source\ndescription: test\n---\n")
            (work / "source-jev").mkdir()
            result = subprocess.run(
                [sys.executable, str(BOOTSTRAP), str(source), "--output-parent", str(work)],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("already exists", result.stderr)


if __name__ == "__main__":
    unittest.main()
