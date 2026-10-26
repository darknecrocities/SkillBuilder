#!/usr/bin/env python3
"""Unit tests for verify_web_ui_hygiene script."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_web_ui_hygiene import (
    audit_web_file,
    WebViolation,
)


class TestVerifyWebUIHygiene(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.test_dir.cleanup()

    def _create_file(self, filename: str, content: str) -> str:
        path = os.path.join(self.test_dir.name, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def test_detects_outline_none_without_focus_visible(self):
        css = """
        button {
            border: none;
            outline: none;
            color: white;
        }
        """
        path = self._create_file("broken.css", css)
        violations = audit_web_file(path)
        rule_ids = [v.rule_id for v in violations]
        self.assertIn("WEB-001", rule_ids)

    def test_detects_inverted_clamp_bounds(self):
        css = """
        h1 {
            font-size: clamp(3rem, 2vw, 1rem);
        }
        """
        path = self._create_file("inverted.css", css)
        violations = audit_web_file(path)
        rule_ids = [v.rule_id for v in violations]
        self.assertIn("WEB-004", rule_ids)

    def test_detects_linear_transition_timing(self):
        css = """
        .card {
            transition: transform 0.2s linear;
        }
        """
        path = self._create_file("linear.css", css)
        violations = audit_web_file(path)
        rule_ids = [v.rule_id for v in violations]
        self.assertIn("WEB-003", rule_ids)

    def test_passes_compliant_web_styling(self):
        css = """
        .card-container {
            container-type: inline-size;
            container-name: card;
        }

        .card {
            background-color: oklch(0.24 0.02 260);
            font-size: clamp(1rem, 0.9rem + 0.5vw, 1.5rem);
            transition: transform 250ms cubic-bezier(0.16, 1, 0.3, 1);
            outline: none;
        }

        .card:focus-visible {
            outline: 2px solid oklch(0.68 0.18 245);
            outline-offset: 2px;
        }
        """
        path = self._create_file("compliant.css", css)
        violations = audit_web_file(path)
        errors = [v for v in violations if v.severity == "ERROR"]
        self.assertEqual(len(errors), 0)


if __name__ == "__main__":
    unittest.main()
