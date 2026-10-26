#!/usr/bin/env python3
"""
Unit tests for verify_firebase_rules.py
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_firebase_rules import audit_firebase_file, scan_firebase_workspace


class TestVerifyFirebaseRules(unittest.TestCase):
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

    def test_clean_rules_pass(self):
        content = """
        rules_version = '2';
        service cloud.firestore {
          match /databases/{db}/documents {
            match /users/{userId} {
              allow read, write: if request.auth != null && request.auth.uid == userId;
            }
          }
        }
        """
        fp = self._write_file("firestore.rules", content)
        violations = audit_firebase_file(fp)
        self.assertEqual(len(violations), 0)

    def test_detects_open_wildcard_rule(self):
        content = """
        rules_version = '2';
        service cloud.firestore {
          match /databases/{db}/documents {
            match /{document=**} {
              allow read, write: if true;
            }
          }
        }
        """
        fp = self._write_file("firestore.rules", content)
        violations = audit_firebase_file(fp)
        self.assertTrue(any(v["rule"] == "FIREBASE-OPEN-WILDCARD-RULE" for v in violations))

    def test_detects_exposed_admin_sdk_key(self):
        content = '{\n  "project_id": "my-firebase-app",\n  "client_email": "firebase-adminsdk-992@app.iam.gserviceaccount.com"\n}'
        fp = self._write_file("admin-key.json", content)
        violations = audit_firebase_file(fp)
        self.assertTrue(any(v["rule"] == "FIREBASE-EXPOSED-ADMIN-KEY" for v in violations))


if __name__ == "__main__":
    unittest.main()
