#!/usr/bin/env python3
"""
Unit tests for sanitize_ai_slop.py
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from sanitize_ai_slop import scan_file


class TestSanitizeAISlop(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def _write_temp(self, filename: str, content: str) -> str:
        path = os.path.join(self.temp_dir.name, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def test_clean_file_passes(self):
        code = """
export async function fetchUser(id: string) {
    if (!id) throw new Error("id required");
    return await db.users.findUnique({ where: { id } });
}
"""
        fp = self._write_temp("clean.ts", code)
        violations = scan_file(fp)
        self.assertEqual(len(violations), 0)

    def test_detects_shields_badge(self):
        code = """# My App\n![Build](https://img.shields.io/badge/build-passing-green)\n"""
        fp = self._write_temp("readme.md", code)
        violations = scan_file(fp)
        self.assertTrue(any(v["rule"] == "ShieldsBadge" for v in violations))

    def test_detects_fake_mock_array(self):
        code = """const mockUsers = [{ id: 1, name: "Alice" }];"""
        fp = self._write_temp("users.ts", code)
        violations = scan_file(fp)
        self.assertTrue(any(v["rule"] == "FakeMockArray" for v in violations))

    def test_detects_obvious_comment(self):
        code = """// set loading to true\nisLoading = true;"""
        fp = self._write_temp("state.ts", code)
        violations = scan_file(fp)
        self.assertTrue(any(v["rule"] == "ObviousComment" for v in violations))

    def test_detects_neon_gradient(self):
        code = """<div className="bg-gradient-to-r from-purple-500 to-indigo-600" />"""
        fp = self._write_temp("card.tsx", code)
        violations = scan_file(fp)
        self.assertTrue(any(v["rule"] == "NeonVibeGradient" for v in violations))

    def test_detects_ai_logo_trope(self):
        code = """<div className="swirling-gradient-sphere" />"""
        fp = self._write_temp("logo.tsx", code)
        violations = scan_file(fp)
        self.assertTrue(any(v["rule"] == "AILogoTrope" for v in violations))

    def test_detects_fuzzy_neon_halo(self):
        code = """.glow { box-shadow: 0 0 50px rgba(168, 85, 247, 0.8); }"""
        fp = self._write_temp("styles.css", code)
        violations = scan_file(fp)
        self.assertTrue(any(v["rule"] == "FuzzyNeonHalo" for v in violations))


if __name__ == "__main__":
    unittest.main()
