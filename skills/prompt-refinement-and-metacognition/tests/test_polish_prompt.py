import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from polish_prompt import polish_prompt, strip_conversational_filler, extract_keywords


class TestPolishPrompt(unittest.TestCase):
    def test_strip_conversational_filler(self):
        sample = "Hey please kindly can you build me a fast login form"
        cleaned = strip_conversational_filler(sample)
        self.assertNotIn("please", cleaned.lower())
        self.assertNotIn("kindly", cleaned.lower())
        self.assertIn("fast login form", cleaned)

    def test_extract_keywords(self):
        text = "I want to build a React application with a FastAPI backend and PostgreSQL database."
        tech = extract_keywords(text)
        self.assertIn("react", tech)
        self.assertIn("fastapi", tech)
        self.assertIn("postgresql", tech)

    def test_polish_prompt_structure(self):
        text = "kindly create a Next.js dashboard with Docker support."
        res = polish_prompt(text)
        self.assertIn("objective", res)
        self.assertIn("detected_stack", res)
        self.assertIn("next.js", res["detected_stack"])
        self.assertIn("docker", res["detected_stack"])
        self.assertIn("Quality & Verification Gates", res["formatted_spec"])


if __name__ == "__main__":
    unittest.main()
