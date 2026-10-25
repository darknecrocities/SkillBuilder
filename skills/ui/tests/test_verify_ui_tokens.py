#!/usr/bin/env python3
"""
Unit tests for verify_ui_tokens.py
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_ui_tokens import audit_ui_content


class TestVerifyUITokens(unittest.TestCase):
    def test_clean_button_passes(self):
        code = """
        <button type="button" className="px-4 py-2 bg-zinc-800 text-zinc-100 rounded">
            <span className="text-xs">Save Changes</span>
        </button>
        """
        violations = audit_ui_content("Button.tsx", code)
        self.assertEqual(len(violations), 0)

    def test_detects_raw_emoji_in_button(self):
        code = '<button type="button">🚀 Deploy Now</button>'
        violations = audit_ui_content("Deploy.tsx", code)
        self.assertTrue(any(v["rule"] == "RAW-EMOJI-IN-UI-CONTROL" for v in violations))

    def test_detects_missing_button_type(self):
        code = '<button className="p-2">Submit</button>'
        violations = audit_ui_content("Form.tsx", code)
        self.assertTrue(any(v["rule"] == "MISSING-BUTTON-TYPE" for v in violations))

    def test_detects_arbitrary_spacing(self):
        code = '<div className="p-[23px] text-zinc-200">Content</div>'
        violations = audit_ui_content("Card.tsx", code)
        self.assertTrue(any(v["rule"] == "ARBITRARY-SPACING-TOKEN" for v in violations))


if __name__ == "__main__":
    unittest.main()
