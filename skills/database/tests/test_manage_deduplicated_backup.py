#!/usr/bin/env python3
"""
Unit tests for manage_deduplicated_backup.py
Verifies content-addressable single-slot backup deduplication (zero spam)
and mandatory human-in-the-loop pre-deletion safety disclosures.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from manage_deduplicated_backup import (
    classify_sensitivity,
    compute_target_sha256,
    ensure_deduplicated_backup,
    evaluate_deletion_safety,
)


class TestManageDeduplicatedBackup(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.backup_dir = self.root / ".backups"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_single_slot_deduplication_prevents_spam(self):
        db_file = self.root / "app_users.sqlite"
        db_file.write_text("CREATE TABLE users (id INT PRIMARY KEY);", encoding="utf-8")

        # First agent creates the canonical backup
        res1 = ensure_deduplicated_backup(
            str(db_file), str(self.backup_dir), agent_id="agent-track-2a"
        )
        self.assertEqual(res1["status"], "CREATED_CANONICAL_BACKUP")
        self.assertFalse(res1["deduplicated"])

        # Second & third concurrent agents run backup on identical state -> zero duplicate files!
        res2 = ensure_deduplicated_backup(
            str(db_file), str(self.backup_dir), agent_id="agent-track-2b"
        )
        res3 = ensure_deduplicated_backup(
            str(db_file), str(self.backup_dir), agent_id="agent-track-2c"
        )
        self.assertEqual(res2["status"], "SKIPPED_DUPLICATE_HASH")
        self.assertTrue(res2["deduplicated"])
        self.assertEqual(res3["status"], "SKIPPED_DUPLICATE_HASH")

        # Ensure only 1 canonical backup file + 1 manifest file exist in .backups/
        backup_files = [p.name for p in self.backup_dir.iterdir()]
        self.assertEqual(sorted(backup_files), ["app_users.sqlite.canonical.bak", "backup_manifest.json"])

    def test_mutated_state_rotates_single_canonical_slot(self):
        db_file = self.root / "ledger.sql"
        db_file.write_text("INSERT INTO ledger VALUES (1, 100);", encoding="utf-8")
        res1 = ensure_deduplicated_backup(str(db_file), str(self.backup_dir))
        hash1 = res1["state_sha256"]

        # Mutate the file
        db_file.write_text("INSERT INTO ledger VALUES (1, 100), (2, 250);", encoding="utf-8")
        res2 = ensure_deduplicated_backup(str(db_file), str(self.backup_dir))
        self.assertEqual(res2["status"], "CREATED_CANONICAL_BACKUP")
        self.assertNotEqual(hash1, res2["state_sha256"])

        # Still only 1 canonical backup file (no .bak.1 or .bak.2 spam)
        bak_slots = [p.name for p in self.backup_dir.iterdir() if p.name.endswith(".bak")]
        self.assertEqual(bak_slots, ["ledger.sql.canonical.bak"])

    def test_deletion_gate_blocks_without_backup_and_user_confirmation(self):
        sensitive_file = self.root / "tenant_invoices.sql"
        sensitive_file.write_text("SELECT * FROM invoices;", encoding="utf-8")

        # 1. No backup & no user confirmation -> blocked
        gate1 = evaluate_deletion_safety(str(sensitive_file), str(self.backup_dir), user_confirmed=False)
        self.assertFalse(gate1["allowed"])
        self.assertFalse(gate1["backup_verified"])
        self.assertIn("Tier 2", gate1["sensitivity_tier"])

        # 2. Backup created, but user has NOT confirmed -> still blocked!
        ensure_deduplicated_backup(str(sensitive_file), str(self.backup_dir))
        gate2 = evaluate_deletion_safety(str(sensitive_file), str(self.backup_dir), user_confirmed=False)
        self.assertTrue(gate2["backup_verified"])
        self.assertFalse(gate2["allowed"])

        # 3. Backup verified AND user explicitly confirmed -> allowed
        gate3 = evaluate_deletion_safety(str(sensitive_file), str(self.backup_dir), user_confirmed=True)
        self.assertTrue(gate3["allowed"])

    def test_sensitivity_classification_tiers(self):
        self.assertIn("Tier 1", classify_sensitivity(".env.production"))
        self.assertIn("Tier 2", classify_sensitivity("customer_wallets.db"))
        self.assertIn("Tier 3", classify_sensitivity("migrations_v2.sql"))


if __name__ == "__main__":
    unittest.main()
