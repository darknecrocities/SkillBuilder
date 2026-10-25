import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from calculate_token_budget import estimate_tokens, analyze_payload


class TestCalculateTokenBudget(unittest.TestCase):
    def test_estimate_tokens_empty(self):
        self.assertEqual(estimate_tokens(""), 0)

    def test_estimate_tokens_non_empty(self):
        text = "Hello world, this is a prompt test for token budget."
        tokens = estimate_tokens(text)
        self.assertGreater(tokens, 0)
        self.assertLess(tokens, len(text))

    def test_analyze_payload_within_budget(self):
        text = "Short prompt payload"
        result = analyze_payload(text, budget_limit=100)
        self.assertEqual(result["status"], "PASS")
        self.assertLess(result["estimated_tokens"], 100)

    def test_analyze_payload_exceeded_budget(self):
        text = "A" * 500
        result = analyze_payload(text, budget_limit=10)
        self.assertEqual(result["status"], "EXCEEDED")


if __name__ == "__main__":
    unittest.main()
