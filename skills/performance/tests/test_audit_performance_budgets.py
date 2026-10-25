#!/usr/bin/env python3
"""
Unit tests for audit_performance_budgets.py
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from audit_performance_budgets import audit_file_performance


class TestAuditPerformanceBudgets(unittest.TestCase):
    def test_clean_batched_query_passes(self):
        code = """
        const userIds = users.map(u => u.id);
        const profiles = await db.profiles.findMany({ where: { userId: { in: userIds } } });
        """
        violations = audit_file_performance("service.ts", code)
        self.assertEqual(len(violations), 0)

    def test_detects_n_plus_one_loop(self):
        code = """
        for user in users:
            profile = db.profiles.find_by_user_id(user.id)
        """
        violations = audit_file_performance("loader.py", code)
        self.assertTrue(any(v["rule"] == "N-PLUS-ONE-QUERY-CASCADE" for v in violations))

    def test_detects_unbounded_select(self):
        code = 'cursor.execute("SELECT * FROM transactions")'
        violations = audit_file_performance("repo.py", code)
        self.assertTrue(any(v["rule"] == "UNBOUNDED-DATABASE-QUERY" for v in violations))

    def test_detects_image_without_dimensions(self):
        code = '<img src="/hero.jpg" alt="Hero banner" />'
        violations = audit_file_performance("Hero.tsx", code)
        self.assertTrue(any(v["rule"] == "IMAGE-MISSING-DIMENSIONS" for v in violations))


if __name__ == "__main__":
    unittest.main()
