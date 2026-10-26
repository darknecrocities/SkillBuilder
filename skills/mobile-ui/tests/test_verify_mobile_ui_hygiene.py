#!/usr/bin/env python3
"""Unit tests for verify_mobile_ui_hygiene script."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_mobile_ui_hygiene import (
    audit_mobile_file,
    MobileViolation,
)


class TestVerifyMobileUIHygiene(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.test_dir.cleanup()

    def _create_file(self, filename: str, content: str) -> str:
        path = os.path.join(self.test_dir.name, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def test_detects_hardcoded_viewport_width(self):
        code = """
        import SwiftUI

        struct BrokenView: View {
            var body: some View {
                VStack {
                    Text("Hello")
                }
                .frame(width: 390)
            }
        }
        """
        path = self._create_file("BrokenView.swift", code)
        violations = audit_mobile_file(path)
        rule_ids = [v.rule_id for v in violations]
        self.assertIn("MOB-001", rule_ids)

    def test_detects_linear_easing_anti_pattern(self):
        code = """
        import SwiftUI

        struct LinearAnimationView: View {
            @State private var isExpanded = false
            var body: some View {
                Circle()
                    .animation(.linear, value: isExpanded)
            }
        }
        """
        path = self._create_file("LinearAnimationView.swift", code)
        violations = audit_mobile_file(path)
        rule_ids = [v.rule_id for v in violations]
        self.assertIn("MOB-002", rule_ids)

    def test_flags_screen_missing_safe_area(self):
        # Must be > 25 lines to trigger screen audit
        lines = ["import SwiftUI\n", "struct ProfileScreen: View {\n"]
        for i in range(25):
            lines.append(f"    var item{i}: String = '{i}'\n")
        lines.append("    var body: some View { Text('Profile') }\n}\n")
        content = "".join(lines)

        path = self._create_file("ProfileScreen.swift", content)
        violations = audit_mobile_file(path)
        rule_ids = [v.rule_id for v in violations]
        self.assertIn("MOB-003", rule_ids)

    def test_passes_compliant_mobile_view(self):
        code = """
        import SwiftUI

        struct CompliantFeedScreen: View {
            @Namespace var feedNamespace
            var body: some View {
                ScrollView {
                    Text("Compliant Feed")
                        .font(.system(.title, design: .rounded))
                }
                .safeAreaInset(edge: .top) {
                    HeaderBar()
                }
                .animation(.spring(response: 0.32, dampingFraction: 0.72), value: true)
            }
        }
        """
        path = self._create_file("CompliantFeedScreen.swift", code)
        violations = audit_mobile_file(path)
        errors = [v for v in violations if v.severity == "ERROR"]
        self.assertEqual(len(errors), 0)


if __name__ == "__main__":
    unittest.main()
