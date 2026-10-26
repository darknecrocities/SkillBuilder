#!/usr/bin/env python3
"""
Unit tests for check_source_line_limits.py
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# Add scripts directory to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from check_source_line_limits import (
    count_physical_lines,
    scan_directory,
    DEFAULT_MAX_LINES,
)


class TestSourceLineLimitChecker(unittest.TestCase):

    def setUp(self) -> None:
        self.temp_dir_obj = tempfile.TemporaryDirectory()
        self.temp_dir = Path(self.temp_dir_obj.name)
        self.script_path = SCRIPT_DIR / "check_source_line_limits.py"

    def tearDown(self) -> None:
        self.temp_dir_obj.cleanup()

    def test_count_physical_lines(self) -> None:
        test_file = self.temp_dir / "sample.py"
        test_file.write_text("line 1\nline 2\nline 3\n", encoding="utf-8")
        self.assertEqual(count_physical_lines(test_file), 3)

        empty_file = self.temp_dir / "empty.py"
        empty_file.write_text("", encoding="utf-8")
        self.assertEqual(count_physical_lines(empty_file), 0)

    def test_scan_directory_clean(self) -> None:
        compliant_file = self.temp_dir / "service.ts"
        compliant_file.write_text("\n".join(f"const x{i} = {i};" for i in range(100)), encoding="utf-8")

        violations, scanned = scan_directory(self.temp_dir, max_lines=500)
        self.assertEqual(len(violations), 0)
        self.assertEqual(len(scanned), 1)

    def test_scan_directory_with_violation(self) -> None:
        long_file = self.temp_dir / "monolith.py"
        long_file.write_text("\n".join(f"# Line {i}" for i in range(550)), encoding="utf-8")

        violations, scanned = scan_directory(self.temp_dir, max_lines=500)
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0]["file"], "monolith.py")
        self.assertEqual(violations[0]["lines"], 550)

    def test_excluded_directories_are_skipped(self) -> None:
        node_modules = self.temp_dir / "node_modules"
        node_modules.mkdir()
        vendor_file = node_modules / "big_dep.js"
        vendor_file.write_text("\n".join(f"console.log({i});" for i in range(600)), encoding="utf-8")

        violations, scanned = scan_directory(self.temp_dir, max_lines=500)
        self.assertEqual(len(violations), 0)
        self.assertEqual(len(scanned), 0)

    def test_extension_filtering(self) -> None:
        markdown_doc = self.temp_dir / "README.md"
        markdown_doc.write_text("\n".join(f"Documentation line {i}" for i in range(700)), encoding="utf-8")

        violations, scanned = scan_directory(self.temp_dir, max_lines=500)
        self.assertEqual(len(violations), 0)
        self.assertEqual(len(scanned), 0)

    def test_cli_exit_code_clean(self) -> None:
        clean_file = self.temp_dir / "clean.py"
        clean_file.write_text("print('hello')\n", encoding="utf-8")

        result = subprocess.run(
            [sys.executable, str(self.script_path), "--path", str(self.temp_dir)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("[PASS]", result.stdout)

    def test_cli_exit_code_violation(self) -> None:
        oversized = self.temp_dir / "oversized.go"
        oversized.write_text("\n".join(f"// line {i}" for i in range(505)), encoding="utf-8")

        result = subprocess.run(
            [sys.executable, str(self.script_path), "--path", str(self.temp_dir)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("[FAIL]", result.stdout)
        self.assertIn("oversized.go", result.stdout)

    def test_cli_json_mode(self) -> None:
        oversized = self.temp_dir / "oversized.ts"
        oversized.write_text("\n".join(f"const a{i} = {i};" for i in range(510)), encoding="utf-8")

        result = subprocess.run(
            [sys.executable, str(self.script_path), "--path", str(self.temp_dir), "--json"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "fail")
        self.assertEqual(payload["violation_count"], 1)
        self.assertEqual(payload["violations"][0]["lines"], 510)

    def test_cli_invalid_path(self) -> None:
        non_existent = self.temp_dir / "non_existent_folder"
        result = subprocess.run(
            [sys.executable, str(self.script_path), "--path", str(non_existent)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 2)

    def test_tier_classification_and_warning(self) -> None:
        warn_file = self.temp_dir / "warning_zone.py"
        warn_file.write_text("\n".join(f"# line {i}" for i in range(380)), encoding="utf-8")

        result = subprocess.run(
            [sys.executable, str(self.script_path), "--path", str(self.temp_dir), "--json"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "pass")
        self.assertEqual(payload["warning_count"], 1)
        self.assertEqual(payload["warnings"][0]["lines"], 380)
        self.assertEqual(payload["tiers"]["warning_count"], 1)


if __name__ == "__main__":
    unittest.main()
