import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_database_hygiene import audit_sql_file


class TestVerifyDatabaseHygiene(unittest.TestCase):
    def test_detects_drop_table(self):
        sql = "DROP TABLE legacy_users;"
        issues = audit_sql_file(sql, "migration.sql")
        self.assertTrue(any(i["rule"] == "DB-HAZARD-DROP-TABLE" for i in issues))

    def test_detects_blocking_index_creation(self):
        sql = "CREATE INDEX idx_users_email ON users(email);"
        issues = audit_sql_file(sql, "migration.sql")
        self.assertTrue(any(i["rule"] == "DB-BLOCKING-INDEX-CREATION" for i in issues))

    def test_passes_concurrent_index(self):
        sql = "CREATE INDEX CONCURRENTLY idx_users_email ON users(email);"
        issues = audit_sql_file(sql, "migration.sql")
        self.assertEqual(len(issues), 0)


if __name__ == "__main__":
    unittest.main()
