import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_api_contracts import audit_route_file


class TestVerifyApiContracts(unittest.TestCase):
    def test_detects_unvalidated_body(self):
        snippet = """
        app.post("/users", (req, res) => {
          const user = db.insert(req.body);
          res.json(user);
        });
        """
        issues = audit_route_file(snippet, "users.ts")
        self.assertTrue(any(i["rule"] == "BE-MISSING-SCHEMA-VALIDATION" for i in issues))

    def test_passes_validated_body(self):
        snippet = """
        app.post("/users", (req, res) => {
          const parsed = UserSchema.safeParse(req.body);
          if (!parsed.success) return res.status(400).json(parsed.error);
          const user = db.insert(parsed.data);
          res.json(user);
        });
        """
        issues = audit_route_file(snippet, "users.ts")
        self.assertEqual(len(issues), 0)

    def test_detects_empty_catch(self):
        snippet = """
        try {
          doWork();
        } catch (e) {}
        """
        issues = audit_route_file(snippet, "worker.ts")
        self.assertTrue(any(i["rule"] == "BE-EMPTY-CATCH-BLOCK" for i in issues))


if __name__ == "__main__":
    unittest.main()
