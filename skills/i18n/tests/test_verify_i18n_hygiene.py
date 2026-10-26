#!/usr/bin/env python3
"""
Unit tests for verify_i18n_hygiene.py
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_i18n_hygiene import audit_i18n_file, scan_i18n_workspace


class TestVerifyI18nHygiene(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def _write_file(self, rel_path: str, content: str) -> str:
        fp = os.path.join(self.temp_dir.name, rel_path)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)
        return fp

    def test_clean_translated_component_passes(self):
        content = """
        export function Header() {
            return <h1>{t('header.title')}</h1>;
        }
        """
        fp = self._write_file("Header.tsx", content)
        violations = audit_i18n_file(fp)
        self.assertEqual(len(violations), 0)

    def test_detects_hardcoded_jsx_string(self):
        content = "<h1>Welcome to the portal!</h1>"
        fp = self._write_file("Hero.tsx", content)
        violations = audit_i18n_file(fp)
        self.assertTrue(any(v["rule"] == "I18N-HARDCODED-UI-STRING" for v in violations))

    def test_detects_physical_css_direction(self):
        content = ".card { margin-left: 20px; }"
        fp = self._write_file("style.css", content)
        violations = audit_i18n_file(fp)
        self.assertTrue(any(v["rule"] == "I18N-PHYSICAL-CSS-DIRECTION" for v in violations))

    def test_detects_ternary_pluralization(self):
        content = "const label = count === 1 ? 'item' : 'items';"
        fp = self._write_file("util.tsx", content)
        violations = audit_i18n_file(fp)
        self.assertTrue(any(v["rule"] == "I18N-TERNARY-PLURALIZATION" for v in violations))


if __name__ == "__main__":
    unittest.main()
