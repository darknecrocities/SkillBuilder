#!/usr/bin/env python3
"""Unit tests for local-first-data and public/private boundary auditor."""

import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import verify_local_first_hygiene  # noqa: E402


class TestVerifyLocalFirstHygiene(unittest.TestCase):
    def test_detects_generated_data_bypass_in_components(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            comp_dir = Path(tmp) / "src" / "components"
            comp_dir.mkdir(parents=True)
            bad = comp_dir / "Card.tsx"
            bad.write_text('import raw from "@/data/generated/civic/projects.json";\n', encoding="utf-8")
            issues = verify_local_first_hygiene.scan_directory(bad)
            self.assertEqual([i["rule"] for i in issues], ["DATA-BOUNDARY-BYPASS"])

    def test_detects_missing_idb_upgrade_handler(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "store.ts"
            bad.write_text('const req = indexedDB.open("local_db", 2);\n', encoding="utf-8")
            issues = verify_local_first_hygiene.scan_directory(bad)
            self.assertEqual([i["rule"] for i in issues], ["IDB-MISSING-MIGRATION-HANDLER"])

    def test_typed_data_accessor_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp) / "src" / "data" / "civic"
            data_dir.mkdir(parents=True)
            good = data_dir / "projects.ts"
            good.write_text('import raw from "@/data/generated/civic/projects.json";\n', encoding="utf-8")
            self.assertEqual(verify_local_first_hygiene.scan_directory(good), [])


if __name__ == "__main__":
    unittest.main()
