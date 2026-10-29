#!/usr/bin/env python3
"""
Unit tests for verify_gcp_hygiene.py
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_gcp_hygiene import audit_gcp_file, scan_gcp_workspace


class TestVerifyGcpHygiene(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def _write_file(self, rel_path: str, content: str) -> str:
        fp = os.path.join(self.temp_dir.name, rel_path)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)
        return fp

    def test_clean_dockerfile_passes(self):
        content = """
        FROM node:20-alpine
        WORKDIR /app
        USER 10001
        CMD ["node", "server.js"]
        """
        fp = self._write_file("Dockerfile", content)
        violations = audit_gcp_file(fp)
        self.assertEqual(len(violations), 0)

    def test_root_dockerfile_flags_violation(self):
        content = """
        FROM node:20-alpine
        WORKDIR /app
        USER root
        CMD ["node", "server.js"]
        """
        fp = self._write_file("Dockerfile", content)
        violations = audit_gcp_file(fp)
        self.assertTrue(any(v["rule"] == "GCP-CONTAINER-ROOT-USER" for v in violations))

    def test_exposed_service_account_flags_violation(self):
        content = '{\n  "type": "service_account",\n  "private_key_id": "12345"\n}'
        fp = self._write_file("credentials.json", content)
        violations = audit_gcp_file(fp)
        self.assertTrue(any(v["rule"] == "GCP-EXPOSED-SERVICE-ACCOUNT-KEY" for v in violations))

    def test_hardcoded_project_flags_violation(self):
        content = 'const path = "projects/123456789012/secrets/my-key";'
        fp = self._write_file("secret.ts", content)
        violations = audit_gcp_file(fp)
        self.assertTrue(any(v["rule"] == "GCP-HARDCODED-PROJECT-ID" for v in violations))

    def test_disabled_deletion_protection_flags_violation(self):
        content = 'resource "google_sql_database_instance" "db" {\n  deletion_protection = false\n}'
        fp = self._write_file("main.tf", content)
        violations = audit_gcp_file(fp)
        self.assertTrue(any(v["rule"] == "GCP-DISABLED-DELETION-PROTECTION" for v in violations))


if __name__ == "__main__":
    unittest.main()
