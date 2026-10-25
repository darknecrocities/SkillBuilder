#!/usr/bin/env python3
"""
Unit tests for verify_app_functionality.py

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder Quality Assurance Framework
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_app_functionality import audit_source_code, is_test_file


class TestVerifyAppFunctionality(unittest.TestCase):
    def test_clean_production_code_passes(self):
        code = """
        import requests
        import logging

        def fetch_weather(lat: float, lon: float):
            try:
                res = requests.get(f"https://api.weather.com/v1?lat={lat}&lon={lon}", timeout=5)
                return res.json()
            except Exception as err:
                logging.error("Failed to fetch weather: %s", err)
                raise
        """
        violations = audit_source_code("service.py", code)
        self.assertEqual(len(violations), 0)

    def test_detects_unbounded_python_request(self):
        code = 'response = requests.get("https://api.example.com/data")'
        violations = audit_source_code("client.py", code)
        self.assertTrue(any(v["rule"] == "UNBOUNDED-NETWORK-CALL" for v in violations))

    def test_passes_bounded_python_request(self):
        code = 'response = requests.get("https://api.example.com/data", timeout=3.0)'
        violations = audit_source_code("client.py", code)
        self.assertEqual(len(violations), 0)

    def test_detects_empty_python_except_block(self):
        code = """
        try:
            do_something()
        except:
            pass
        """
        violations = audit_source_code("worker.py", code)
        self.assertTrue(any(v["rule"] == "UNHANDLED-EMPTY-CATCH" for v in violations))

    def test_detects_empty_js_catch_block(self):
        code = """
        try {
            await doSomething();
        } catch (err) {}
        """
        violations = audit_source_code("handler.ts", code)
        self.assertTrue(any(v["rule"] == "UNHANDLED-EMPTY-CATCH" for v in violations))

    def test_detects_hardcoded_secret_in_production(self):
        code = 'api_key = "test_custom_service_key_9876543210_abcdef"'
        violations = audit_source_code("auth.py", code)
        self.assertTrue(any(v["rule"] == "HARDCODED-SECRET-LITERAL" for v in violations))

    def test_allows_secret_in_test_file(self):
        code = 'api_key = "test_custom_service_key_9876543210_abcdef"'
        violations = audit_source_code("tests/test_auth.py", code)
        self.assertEqual(len(violations), 0)

    def test_detects_fake_mock_storage_in_production(self):
        code = "const " + "mockUsers = [{ id: 1, name: 'Alice' }];"
        violations = audit_source_code("userService.ts", code)
        self.assertTrue(any(v["rule"] == "FAKE-MOCK-STORAGE" for v in violations))

    def test_allows_mock_storage_in_test_file(self):
        code = "const " + "mockUsers = [{ id: 1, name: 'Alice' }];"
        violations = audit_source_code("tests/userService.test.ts", code)
        self.assertEqual(len(violations), 0)

    def test_is_test_file_helper(self):
        self.assertTrue(is_test_file("skills/qa/tests/test_something.py"))
        self.assertTrue(is_test_file("src/components/Button.test.tsx"))
        self.assertTrue(is_test_file("src/api/auth.spec.ts"))
        self.assertFalse(is_test_file("src/components/Button.tsx"))
        self.assertFalse(is_test_file("skills/qa/scripts/verify_app_functionality.py"))


if __name__ == "__main__":
    unittest.main()
