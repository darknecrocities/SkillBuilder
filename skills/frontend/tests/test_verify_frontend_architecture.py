#!/usr/bin/env python3
"""
Unit tests for verify_frontend_architecture.py
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_frontend_architecture import audit_component_file


class TestVerifyFrontendArchitecture(unittest.TestCase):
    def test_clean_effect_with_abort_passes(self):
        code = """
        useEffect(() => {
            const controller = new AbortController();
            fetch('/api/data', { signal: controller.signal });
            return () => controller.abort();
        }, []);
        """
        violations = audit_component_file("Component.tsx", code)
        self.assertEqual(len(violations), 0)

    def test_detects_unprotected_fetch_in_effect(self):
        code = """
        useEffect(() => {
            fetch('/api/unprotected');
        }, []);
        """
        violations = audit_component_file("Leaky.tsx", code)
        self.assertTrue(any(v["rule"] == "UNPROTECTED-ASYNC-EFFECT" for v in violations))

    def test_detects_direct_window_mutation(self):
        code = "window.currentSessionUser = { name: 'Alice' };"
        violations = audit_component_file("Store.ts", code)
        self.assertTrue(any(v["rule"] == "DIRECT-WINDOW-MUTATION" for v in violations))


if __name__ == "__main__":
    unittest.main()
