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

    def test_detects_truncate_and_unbounded_delete(self):
        sql = "TRUNCATE TABLE invoices;\nDELETE FROM users;"
        issues = audit_sql_file(sql, "purge.sql")
        rules = {i["rule"] for i in issues}
        self.assertIn("DB-HAZARD-TRUNCATE-TABLE", rules)
        self.assertIn("DB-HAZARD-UNBOUNDED-DELETE", rules)

    def test_passes_approved_deletion_with_verified_backup_hash(self):
        sql = (
            "-- @user-approved-deletion\n"
            "-- @verified-backup-sha256: e3b0c44298fc1c149afbf4c8996fb924\n"
            "DROP TABLE legacy_users;"
        )
        issues = audit_sql_file(sql, "approved_migration.sql")
        self.assertEqual(len(issues), 0)

    def test_detects_spam_duplicate_backup_filename(self):
        sql = "SELECT 1;"
        issues = audit_sql_file(sql, "db_backup_2.sql")
        self.assertTrue(any(i["rule"] == "DB-SPAM-DUPLICATE-BACKUP" for i in issues))


if __name__ == "__main__":
    unittest.main()
