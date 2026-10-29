#!/usr/bin/env python3
"""
Unit tests for skill_linter.py

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder Quality & Optimization Engine
"""

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from skill_linter import (
    audit_anti_slop,
    audit_frontmatter,
    audit_markdown_links,
    audit_single_skill,
    estimate_tokens,
)


class TestSkillLinter(unittest.TestCase):
    def test_estimate_tokens(self):
        self.assertEqual(estimate_tokens(""), 0)
        self.assertGreater(estimate_tokens("Hello world"), 1)

    def test_audit_frontmatter_valid_and_invalid(self):
        valid_doc = "---\nname: my-skill\ndescription: A valid descriptive trigger for my specialized skill.\n---\n# Content"
        valid, msg, meta = audit_frontmatter(valid_doc, "my-skill")
        self.assertTrue(valid)
        self.assertEqual(meta["name"], "my-skill")

        # Missing name
        invalid_doc = "---\ndescription: Missing name\n---\n# Content"
        valid, msg, _ = audit_frontmatter(invalid_doc, "my-skill")
        self.assertFalse(valid)
        self.assertIn("Missing 'name'", msg)

        # Folded scalar description
        folded_doc = "---\nname: folded-skill\ndescription: >-\n  This is a multiline folded description that exceeds 25 characters.\n---\n# Content"
        valid, msg, meta = audit_frontmatter(folded_doc, "folded-skill")
        self.assertTrue(valid)
        self.assertIn("multiline folded description", meta["description"])

    def test_audit_markdown_links(self):
        with tempfile.TemporaryDirectory() as td:
            folder = Path(td)
            (folder / "references").mkdir()
            (folder / "references" / "guide.md").write_text("# Guide", encoding="utf-8")

            content = "Read [guide](references/guide.md) and [missing](references/missing.md)"
            violations = audit_markdown_links(folder, content)
            self.assertEqual(len(violations), 1)
            self.assertEqual(violations[0]["rule"], "BROKEN-MARKDOWN-LINK")

    def test_audit_anti_slop(self):
        slop_badge = "![Badge](https://img.shields.io/badge/status-active-green)"
        violations = audit_anti_slop(slop_badge)
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0]["rule"], "DECORATIVE-BADGE-SLOP")

        # Prohibited mock array vs anti-pattern mention
        prohibited = "const users = [{ id: 1, name: 'Alice' }];"
        violations = audit_anti_slop(prohibited)
        self.assertEqual(len(violations), 1)

        allowed_mention = "Never do: const users = [{ id: 1, name: 'Alice' }];"
        clean_violations = audit_anti_slop(allowed_mention)
        self.assertEqual(len(clean_violations), 0)


if __name__ == "__main__":
    unittest.main()
