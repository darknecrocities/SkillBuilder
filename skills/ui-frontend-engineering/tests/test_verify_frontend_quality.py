import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_frontend_quality import audit_component_content


class TestVerifyFrontendQuality(unittest.TestCase):
    def test_detects_img_missing_alt(self):
        snippet = '<div className="hero"><img src="/banner.png" className="w-full" /></div>'
        issues = audit_component_content(snippet, "test.tsx")
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["rule"], "A11Y-IMG-ALT")

    def test_passes_img_with_alt(self):
        snippet = '<img src="/banner.png" alt="Company dashboard banner" />'
        issues = audit_component_content(snippet, "test.tsx")
        self.assertEqual(len(issues), 0)

    def test_detects_button_without_label(self):
        snippet = '<button className="icon-btn"><svg></svg></button>'
        issues = audit_component_content(snippet, "test.tsx")
        self.assertTrue(any(i["rule"] == "A11Y-BUTTON-NAME" for i in issues))

    def test_passes_button_with_aria_label(self):
        snippet = '<button aria-label="Open sidebar"><svg></svg></button>'
        issues = audit_component_content(snippet, "test.tsx")
        self.assertEqual(len(issues), 0)


if __name__ == "__main__":
    unittest.main()
