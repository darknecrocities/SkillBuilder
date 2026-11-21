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
        self.assertGreaterEqual(len(skills), 48, f"Expected at least 48 skills, found {len(skills)}")
        names = [s[0] for s in skills]
        self.assertIn("darknecrostack", names)
        self.assertIn("code-archaeology", names)
        self.assertIn("architect", names)
        self.assertIn("arena", names)
        self.assertIn("interrogate", names)
        self.assertIn("prove-it-works", names)
        self.assertIn("2d-mascot-motion", names)
        self.assertIn("brand-assets", names)
        self.assertIn("mcp-engineering", names)
        self.assertIn("browser-media-wasm", names)
        self.assertIn("local-first-data", names)
        self.assertIn("video-editing", names)

    def test_export_cursor_rules(self):
        skills = get_all_skills(self.repo_dir)
        created = export_cursor_rules(self.repo_dir, self.temp_path)
        self.assertTrue(len(created) >= len(skills) + 1)  # .mdc + .cursorrules
        cursorrules_file = self.temp_path / ".cursorrules"
        self.assertTrue(cursorrules_file.exists())
        content = cursorrules_file.read_text(encoding="utf-8")
        self.assertIn(f"{len(skills)} Modular Skills Available", content)
        self.assertNotIn("20 Modular Skills", content)
        self.assertTrue((self.temp_path / ".cursor" / "rules" / "anti-slop.mdc").exists())
        self.assertTrue((self.temp_path / ".cursor" / "rules" / "antigravity-automation.mdc").exists())
        self.assertTrue((self.temp_path / ".cursor" / "rules" / "video-editing.mdc").exists())

    def test_export_claude_rules(self):
        skills = get_all_skills(self.repo_dir)
        created = export_claude_rules(self.repo_dir, self.temp_path)
        self.assertEqual(len(created), 1)
        claude_file = self.temp_path / "CLAUDE.md"
        self.assertTrue(claude_file.exists())
        content = claude_file.read_text(encoding="utf-8")
        self.assertIn("DarkNecroStack", content)
        self.assertIn("/darknecrostack", content)
        self.assertIn("/2d-mascot-motion", content)
        self.assertIn("/brand-assets", content)
        self.assertIn("/anti-slop", content)
        self.assertIn("/antigravity-automation", content)
        self.assertIn("/video-editing", content)
        self.assertIn(f"({len(skills)} Skills)", content)
        self.assertNotIn("(20 Skills)", content)
        self.assertIn("Idempotent Single-Slot Backups", content)
        self.assertIn("Sensitive Deletion Human-in-the-Loop Gate", content)

    def test_export_codex_rules(self):
        skills = get_all_skills(self.repo_dir)
        created = export_codex_rules(self.repo_dir, self.temp_path)
        self.assertEqual(len(created), 1)
        codex_file = self.temp_path / "CODEX.md"
        self.assertTrue(codex_file.exists())
        content = codex_file.read_text(encoding="utf-8")
        self.assertIn("CODEX.md", content)
        self.assertIn("/antigravity-automation", content)
        self.assertIn("/video-editing", content)
        self.assertIn(f"({len(skills)} Skills)", content)
        self.assertNotIn("(20 Skills)", content)
        self.assertIn("Sensitive Deletion Gate", content)


if __name__ == "__main__":
    unittest.main()
