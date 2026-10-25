#!/usr/bin/env python3
"""
Unit tests for verify_responsiveness_and_qa.py
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_responsiveness_and_qa import audit_file_content, check_html_viewport_meta


class TestVerifyResponsivenessAndQA(unittest.TestCase):
    def test_clean_responsive_component_passes(self):
        code = """
        <div className="w-full max-w-5xl mx-auto px-4 grid grid-cols-1 md:grid-cols-3 gap-6">
            <button className="px-4 py-2 min-h-[44px] rounded bg-zinc-800 text-zinc-100 focus-visible:ring-2 focus-visible:ring-zinc-400">
                Action
            </button>
        </div>
        """
        violations = audit_file_content("Component.tsx", code)
        self.assertEqual(len(violations), 0)

    def test_detects_fixed_pixel_width(self):
        code = '<div className="w-[850px] bg-zinc-900">'
        violations = audit_file_content("Card.tsx", code)
        self.assertTrue(any(v["rule"] == "FIXED-PIXEL-CONTAINER-WIDTH" for v in violations))

    def test_detects_missing_focus_ring(self):
        code = '<button className="outline-none text-zinc-200">Click</button>'
        violations = audit_file_content("Button.tsx", code)
        self.assertTrue(any(v["rule"] == "MISSING-FOCUS-RING" for v in violations))

    def test_detects_unresponsive_grid(self):
        code = '<div className="grid grid-cols-4 gap-4">'
        violations = audit_file_content("Grid.tsx", code)
        self.assertTrue(any(v["rule"] == "UNRESPONSIVE-GRID-COLUMNS" for v in violations))

    def test_detects_missing_viewport_in_html(self):
        html = "<!DOCTYPE html><html><head><title>Test</title></head><body></body></html>"
        violations = check_html_viewport_meta("index.html", html)
        self.assertTrue(any(v["rule"] == "MISSING-VIEWPORT-META" for v in violations))

    def test_passes_valid_viewport_in_html(self):
        html = '<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Test</title></head></html>'
        violations = check_html_viewport_meta("index.html", html)
        self.assertEqual(len(violations), 0)


if __name__ == "__main__":
    unittest.main()
