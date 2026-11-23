#!/usr/bin/env python3
"""Unit tests for verify_ab_experiment.py."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_ab_experiment import audit_ab_file, check_srm, check_two_proportion_ztest


class TestVerifyABExperiment(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _write(self, name: str, content: str) -> str:
        path = os.path.join(self.tmp.name, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def test_detects_random_bucketing_and_missing_guardrail(self) -> None:
        code = (
            "const experiment_id = 'checkout_v2';\n"
            "const variant = Math.random() < 0.5 ? 'control' : 'treatment';\n"
            "track_exposure(variant);\n"
        )
        violations = audit_ab_file(self._write("bad_ab.ts", code))
        rules = {v.rule_id for v in violations}
        self.assertIn("AB-001", rules)
        self.assertIn("AB-002", rules)
        self.assertIn("AB-003", rules)

    def test_compliant_hash_bucketing_passes(self) -> None:
        code = (
            "import hashlib\n"
            "experiment_id = 'rag_rerank_v1'\n"
            "guardrail_metrics = ['p95_latency_ms', 'error_rate']\n"
            "def bucket(uid: str) -> str:\n"
            "    h = hashlib.sha256(f'{experiment_id}:{uid}'.encode()).digest()\n"
            "    return 'treatment' if int.from_bytes(h[:4], 'big') % 10000 < 5000 else 'control'\n"
            "def log_it(uid: str):\n"
            "    track_exposure(experiment_id=experiment_id, variant=bucket(uid))\n"
        )
        violations = audit_ab_file(self._write("good_ab.py", code))
        self.assertEqual(len(violations), 0)

    def test_srm_and_ztest_statistics(self) -> None:
        srm_bad = check_srm(5000, 4400, 0.5)
        self.assertTrue(srm_bad["srm_detected"])
        self.assertEqual(srm_bad["status"], "SRM_HALT")

        srm_ok = check_srm(5012, 4988, 0.5)
        self.assertFalse(srm_ok["srm_detected"])

        z_sig = check_two_proportion_ztest(5000, 500, 5000, 620)
        self.assertTrue(z_sig["significant"])
        self.assertGreater(z_sig["rel_lift_pct"], 20.0)


if __name__ == "__main__":
    unittest.main()
