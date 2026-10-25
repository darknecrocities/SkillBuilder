#!/usr/bin/env python3
"""
Unit tests for detect_refactor_opportunities.py
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from detect_refactor_opportunities import audit_file_complexity


class TestDetectRefactorOpportunities(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def _write_temp(self, filename: str, content: str) -> str:
        fp = os.path.join(self.temp_dir.name, filename)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)
        return fp

    def test_clean_small_function_passes(self):
        code = """
        def add(a, b):
            return a + b
        """
        fp = self._write_temp("clean.py", code)
        violations = audit_file_complexity(fp)
        self.assertEqual(len(violations), 0)

    def test_detects_deep_nesting(self):
        code = """
        def deep():
            if True:
                if True:
                    if True:
                        if True:
                            if True:
                                print('too deep')
        """
        fp = self._write_temp("nested.py", code)
        violations = audit_file_complexity(fp)
        self.assertTrue(any(v["rule"] == "DEEP-LOGICAL-NESTING" for v in violations))

    def test_detects_file_nearing_limit(self):
        code = "\n".join(["# line" for _ in range(420)])
        fp = self._write_temp("large.py", code)
        violations = audit_file_complexity(fp)
        self.assertTrue(any(v["rule"] == "FILE-NEARING-LINE-LIMIT" for v in violations))


if __name__ == "__main__":
    unittest.main()
