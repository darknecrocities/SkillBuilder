#!/usr/bin/env python3
"""
Unit tests for research_alternatives.py
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from research_alternatives import audit_manifest, find_alternative


class TestResearchAlternatives(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_find_alternative_moment(self):
        result = find_alternative("moment")
        self.assertIsNotNone(result)
        self.assertEqual(result["status"], "deprecated")
        self.assertIn("date-fns", result["recommended"])

    def test_find_alternative_request(self):
        result = find_alternative("request")
        self.assertIsNotNone(result)
        self.assertIn("native fetch", result["recommended"])

    def test_find_alternative_unknown(self):
        result = find_alternative("non_existent_pkg_xyz_999")
        self.assertIsNone(result)

    def test_audit_manifest_detects_deprecated(self):
        pkg_json = os.path.join(self.temp_dir.name, "package.json")
        with open(pkg_json, "w", encoding="utf-8") as f:
            f.write('{"dependencies": {"moment": "^2.29.4", "react": "^18.2.0"}}')

        findings = audit_manifest(pkg_json)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["package"], "moment")

    def test_audit_manifest_clean(self):
        pkg_json = os.path.join(self.temp_dir.name, "package.json")
        with open(pkg_json, "w", encoding="utf-8") as f:
            f.write('{"dependencies": {"date-fns": "^3.0.0", "react": "^18.2.0"}}')

        findings = audit_manifest(pkg_json)
        self.assertEqual(len(findings), 0)


if __name__ == "__main__":
    unittest.main()
