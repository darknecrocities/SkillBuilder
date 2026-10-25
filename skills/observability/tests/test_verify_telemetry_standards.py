#!/usr/bin/env python3
"""
Unit tests for verify_telemetry_standards.py
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_telemetry_standards import audit_file_telemetry


class TestVerifyTelemetryStandards(unittest.TestCase):
    def test_structured_logger_passes(self):
        code = """
        logger.info("Payment processed", extra={"trace_id": trace_id, "amount": 100})
        """
        violations = audit_file_telemetry("src/billing/service.py", code)
        self.assertEqual(len(violations), 0)

    def test_detects_raw_print_in_service(self):
        code = """
        def process_order(order):
            print("Processing order: " + str(order))
        """
        violations = audit_file_telemetry("src/orders/service.py", code)
        self.assertTrue(any(v["rule"] == "RAW-PRINT-IN-PRODUCTION" for v in violations))


if __name__ == "__main__":
    unittest.main()
