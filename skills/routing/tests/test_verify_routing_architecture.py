#!/usr/bin/env python3
"""
Unit tests for verify_routing_architecture.py
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_routing_architecture import audit_routing_directory


class TestVerifyRoutingArchitecture(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def _write_file(self, rel_path: str, content: str = "// stub") -> str:
        fp = os.path.join(self.temp_dir.name, rel_path)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)
        return fp

    def test_clean_route_tree_passes(self):
        self._write_file("app/layout.tsx")
        self._write_file("app/page.tsx")
        self._write_file("app/projects/[id]/page.tsx", "export default function P() { return null; }")
        self._write_file("app/projects/[id]/loading.tsx")
        self._write_file("app/projects/[id]/error.tsx")

        violations = audit_routing_directory(os.path.join(self.temp_dir.name, "app"))
        self.assertEqual(len(violations), 0)

    def test_detects_missing_loading_boundary(self):
        self._write_file("app/users/[userId]/page.tsx")
        self._write_file("app/users/[userId]/error.tsx")

        violations = audit_routing_directory(os.path.join(self.temp_dir.name, "app"))
        self.assertTrue(any(v["rule"] == "ROUTING-MISSING-LOADING-BOUNDARY" for v in violations))

    def test_detects_missing_error_boundary(self):
        self._write_file("app/orgs/[orgId]/page.tsx")
        self._write_file("app/orgs/[orgId]/loading.tsx")

        violations = audit_routing_directory(os.path.join(self.temp_dir.name, "app"))
        self.assertTrue(any(v["rule"] == "ROUTING-MISSING-ERROR-BOUNDARY" for v in violations))

    def test_detects_excessive_layout_depth(self):
        deep_path = "app/a/b/c/d/e/page.tsx"
        self._write_file(deep_path)

        violations = audit_routing_directory(os.path.join(self.temp_dir.name, "app"))
        self.assertTrue(any(v["rule"] == "ROUTING-EXCESSIVE-LAYOUT-DEPTH" for v in violations))


if __name__ == "__main__":
    unittest.main()
