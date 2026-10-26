#!/usr/bin/env python3
"""
Unit tests for verify_testing_hygiene.py
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_testing_hygiene import audit_test_file, scan_testing_workspace


class TestVerifyTestingHygiene(unittest.TestCase):
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

    def test_clean_accessible_test_passes(self):
        content = """
        test('logs in cleanly', async ({ page }) => {
            await page.getByRole('button', { name: 'Submit' }).click();
            await expect(page.getByText('Success')).toBeVisible();
        });
        """
        fp = self._write_file("tests/auth.spec.ts", content)
        violations = audit_test_file(fp)
        self.assertEqual(len(violations), 0)

    def test_detects_arbitrary_sleep_timer(self):
        content = """
        test('flaky wait', async ({ page }) => {
            await page.waitForTimeout(5000);
            expect(true).toBe(true);
        });
        """
        fp = self._write_file("tests/flaky.spec.ts", content)
        violations = audit_test_file(fp)
        self.assertTrue(any(v["rule"] == "TESTING-ARBITRARY-SLEEP-TIMER" for v in violations))

    def test_detects_fragile_css_locator(self):
        content = """
        test('clicks button', async ({ page }) => {
            await page.click('div.container>button.submit-btn');
        });
        """
        fp = self._write_file("tests/fragile.spec.ts", content)
        violations = audit_test_file(fp)
        self.assertTrue(any(v["rule"] == "TESTING-FRAGILE-CSS-SELECTOR" for v in violations))


if __name__ == "__main__":
    unittest.main()
