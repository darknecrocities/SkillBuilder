#!/usr/bin/env python3
"""
Unit tests for scaffold_project_hygiene.py
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from scaffold_project_hygiene import (
    audit_project,
    apply_hygiene,
    detect_ecosystem,
)


class TestProjectHygieneScaffolder(unittest.TestCase):

    def setUp(self) -> None:
        self.temp_dir_obj = tempfile.TemporaryDirectory()
        self.temp_dir = Path(self.temp_dir_obj.name)
        self.script_path = SCRIPT_DIR / "scaffold_project_hygiene.py"

    def tearDown(self) -> None:
        self.temp_dir_obj.cleanup()

    def test_detect_ecosystem(self) -> None:
        # Default generic
        self.assertEqual(detect_ecosystem(self.temp_dir), "generic")

        # Node
        (self.temp_dir / "package.json").write_text("{}", encoding="utf-8")
        self.assertEqual(detect_ecosystem(self.temp_dir), "node")
        (self.temp_dir / "package.json").unlink()

        # Python
        (self.temp_dir / "requirements.txt").write_text("", encoding="utf-8")
        self.assertEqual(detect_ecosystem(self.temp_dir), "python")
        (self.temp_dir / "requirements.txt").unlink()

        # Go
        (self.temp_dir / "go.mod").write_text("module example.com/app", encoding="utf-8")
        self.assertEqual(detect_ecosystem(self.temp_dir), "go")

    def test_audit_missing_and_applied(self) -> None:
        audit = audit_project(self.temp_dir)
        self.assertFalse(all(audit.values()))
        self.assertFalse(audit[".gitignore"])
        self.assertFalse(audit["Dockerfile"])

        # Apply hygiene
        created = apply_hygiene(self.temp_dir, ecosystem="node")
        self.assertEqual(len(created), 7)

        # Audit should now be 100% compliant
        updated_audit = audit_project(self.temp_dir)
        self.assertTrue(all(updated_audit.values()))

    def test_apply_does_not_overwrite(self) -> None:
        custom_gitignore = "# Custom user ignore"
        (self.temp_dir / ".gitignore").write_text(custom_gitignore, encoding="utf-8")

        created = apply_hygiene(self.temp_dir, ecosystem="python")
        self.assertNotIn(".gitignore", created)
        self.assertEqual((self.temp_dir / ".gitignore").read_text(encoding="utf-8"), custom_gitignore)

    def test_cli_check_returns_nonzero_when_missing(self) -> None:
        result = subprocess.run(
            [sys.executable, str(self.script_path), "--path", str(self.temp_dir), "--check"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("[MISSING]", result.stdout)

    def test_cli_apply_returns_zero(self) -> None:
        result = subprocess.run(
            [sys.executable, str(self.script_path), "--path", str(self.temp_dir), "--apply"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("[APPLIED]", result.stdout)

        # Subsequent check should return 0
        check_result = subprocess.run(
            [sys.executable, str(self.script_path), "--path", str(self.temp_dir), "--check"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(check_result.returncode, 0)
        self.assertIn("[PASS]", check_result.stdout)

    def test_cli_json_output(self) -> None:
        result = subprocess.run(
            [sys.executable, str(self.script_path), "--path", str(self.temp_dir), "--check", "--json"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "fail")
        self.assertIn(".gitignore", payload["missing_files"])


if __name__ == "__main__":
    unittest.main()
