#!/usr/bin/env python3
"""
Unit tests for synthesize_project_skill.py
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from synthesize_project_skill import (
    detect_project_profile,
    generate_skill_markdown,
    mint_project_skill,
)


class TestSynthesizeProjectSkill(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_detects_node_project_with_supabase(self):
        pkg_data = {
            "name": "acme-saas",
            "dependencies": {
                "next": "^15.0.0",
                "@supabase/supabase-js": "^2.39.0"
            },
            "devDependencies": {
                "vitest": "^2.0.0"
            }
        }
        (self.root_path / "package.json").write_text(json.dumps(pkg_data), encoding="utf-8")
        (self.root_path / "src").mkdir()

        profile = detect_project_profile(self.root_path)
        self.assertEqual(profile["name"], "acme-saas")
        self.assertEqual(profile["ecosystem"], "node")
        self.assertIn("Next.js", profile["frameworks"])
        self.assertEqual(profile["persistence"], "Supabase")
        self.assertEqual(profile["testing"], "Vitest")
        self.assertIn("src", profile["directories"])

    def test_generates_valid_markdown_skill(self):
        profile = {
            "name": "payment-service",
            "ecosystem": "node",
            "frameworks": ["Express"],
            "persistence": "Prisma",
            "testing": "Jest",
            "directories": ["src", "prisma"]
        }
        md = generate_skill_markdown(profile)
        self.assertTrue(md.startswith("---"))
        self.assertIn("name: payment-service-domain", md)
        self.assertIn("Prisma", md)
        self.assertIn("500-line ceiling", md)

    def test_mints_skill_file(self):
        profile = {
            "name": "inventory-app",
            "ecosystem": "flutter",
            "frameworks": ["Flutter"],
            "persistence": "Firebase",
            "testing": "flutter_test",
            "directories": ["lib", "test"]
        }
        minted = mint_project_skill(self.root_path, profile)
        self.assertTrue(minted.exists())
        self.assertEqual(minted.name, "SKILL.md")
        content = minted.read_text(encoding="utf-8")
        self.assertIn("inventory-app-domain", content)


if __name__ == "__main__":
    unittest.main()
