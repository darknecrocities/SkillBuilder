#!/usr/bin/env python3
"""
Unit tests for verify_aws_hygiene.py
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_aws_hygiene import audit_aws_file, scan_aws_workspace


class TestVerifyAwsHygiene(unittest.TestCase):
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

    def test_clean_s3_bucket_passes(self):
        content = """
        const bucket = new s3.Bucket(this, "SafeBucket", {
            blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
            encryption: s3.BucketEncryption.S3_MANAGED
        });
        """
        fp = self._write_file("storage.ts", content)
        violations = audit_aws_file(fp)
        self.assertEqual(len(violations), 0)

    def test_detects_static_aws_key(self):
        content = 'const keyId = "AKIA1234567890ABCDEF";'
        fp = self._write_file("client.ts", content)
        violations = audit_aws_file(fp)
        self.assertTrue(any(v["rule"] == "AWS-STATIC-ACCESS-KEY" for v in violations))

    def test_detects_public_s3_acl(self):
        content = 'resource "aws_s3_bucket" "b" { acl = "public-read" }'
        fp = self._write_file("main.tf", content)
        violations = audit_aws_file(fp)
        self.assertTrue(any(v["rule"] == "AWS-S3-PUBLIC-EXPOSURE" for v in violations))

    def test_detects_missing_public_block(self):
        content = """
        const bucket = new s3.Bucket(this, "UnsafeBucket", {
            versioned: true
        });
        """
        fp = self._write_file("stack.ts", content)
        violations = audit_aws_file(fp)
        self.assertTrue(any(v["rule"] == "AWS-S3-MISSING-PUBLIC-BLOCK" for v in violations))


if __name__ == "__main__":
    unittest.main()
