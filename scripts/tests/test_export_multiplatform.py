#!/usr/bin/env python3
"""
Unit tests for export_multiplatform.py
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from export_multiplatform import (
    export_all,
    export_claude_rules,
    export_codex_rules,
    export_cursor_rules,
    get_all_skills,
    parse_skill_metadata,
)


class TestExportMultiplatform(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        self.repo_dir = Path(__file__).resolve().parent.parent.parent

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_get_all_skills(self):
        skills = get_all_skills(self.repo_dir)
        self.assertEqual(len(skills), 20, f"Expected 20 skills, found {len(skills)}")
        names = [s[0] for s in skills]
        self.assertIn("anti-slop", names)
        self.assertIn("world-class-engineering", names)
        self.assertIn("research", names)
        self.assertIn("qa", names)

    def test_export_cursor_rules(self):
        created = export_cursor_rules(self.repo_dir, self.temp_path)
        self.assertTrue(len(created) >= 21)  # 20 .mdc + .cursorrules
        self.assertTrue((self.temp_path / ".cursorrules").exists())
        self.assertTrue((self.temp_path / ".cursor" / "rules" / "anti-slop.mdc").exists())

    def test_export_claude_rules(self):
        created = export_claude_rules(self.repo_dir, self.temp_path)
        self.assertEqual(len(created), 1)
        claude_file = self.temp_path / "CLAUDE.md"
        self.assertTrue(claude_file.exists())
        content = claude_file.read_text(encoding="utf-8")
        self.assertIn("SkillBuilder", content)
        self.assertIn("/anti-slop", content)

    def test_export_codex_rules(self):
        created = export_codex_rules(self.repo_dir, self.temp_path)
        self.assertEqual(len(created), 1)
        codex_file = self.temp_path / "CODEX.md"
        self.assertTrue(codex_file.exists())
        content = codex_file.read_text(encoding="utf-8")
        self.assertIn("CODEX.md", content)


if __name__ == "__main__":
    unittest.main()
