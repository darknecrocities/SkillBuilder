#!/usr/bin/env python3
"""
Unit tests for audit_security_hygiene.py
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from audit_security_hygiene import audit_file


class TestAuditSecurityHygiene(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def _write_temp(self, filename: str, content: str) -> str:
        fp = os.path.join(self.temp_dir.name, filename)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)
        return fp

    def test_clean_parameterized_query_passes(self):
        code = """
        cursor.execute("SELECT id, name FROM users WHERE id = %s", (user_id,))
        """
        fp = self._write_temp("repo.py", code)
        violations = audit_file(fp)
        self.assertEqual(len(violations), 0)

    def test_detects_unsafe_sql_interpolation(self):
        code = 'db.execute(f"SELECT * FROM users WHERE id = {user_id}")'
        fp = self._write_temp("vulnerable.py", code)
        violations = audit_file(fp)
        self.assertTrue(any(v["rule"] == "UNSAFE-SQL-INTERPOLATION" for v in violations))

    def test_detects_shell_true(self):
        code = 'subprocess.Popen("ls -la", shell=True)'
        fp = self._write_temp("runner.py", code)
        violations = audit_file(fp)
        self.assertTrue(any(v["rule"] == "UNSAFE-SHELL-TRUE" for v in violations))

    def test_detects_eval(self):
        code = 'result = eval(user_input)'
        fp = self._write_temp("eval.py", code)
        violations = audit_file(fp)
        self.assertTrue(any(v["rule"] == "UNSAFE-EVAL-EXEC" for v in violations))


if __name__ == "__main__":
    unittest.main()
