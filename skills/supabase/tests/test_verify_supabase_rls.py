#!/usr/bin/env python3
"""
Unit tests for verify_supabase_rls.py
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_supabase_rls import audit_supabase_file, scan_supabase_workspace


class TestVerifySupabaseRls(unittest.TestCase):
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

    def test_clean_migration_passes(self):
        content = """
        CREATE TABLE public.todos (
            id UUID PRIMARY KEY,
            title TEXT NOT NULL
        );
        ALTER TABLE public.todos ENABLE ROW LEVEL SECURITY;
        CREATE POLICY "Owner read" ON public.todos FOR SELECT USING (auth.uid() = id);
        """
        fp = self._write_file("001_create_todos.sql", content)
        violations = audit_supabase_file(fp)
        self.assertEqual(len(violations), 0)

    def test_detects_missing_rls(self):
        content = """
        CREATE TABLE public.invoices (
            id UUID PRIMARY KEY,
            amount NUMERIC NOT NULL
        );
        """
        fp = self._write_file("002_create_invoices.sql", content)
        violations = audit_supabase_file(fp)
        self.assertTrue(any(v["rule"] == "SUPABASE-MISSING-RLS" for v in violations))

    def test_detects_permissive_policy(self):
        content = """
        CREATE TABLE public.logs (id UUID PRIMARY KEY);
        ALTER TABLE public.logs ENABLE ROW LEVEL SECURITY;
        CREATE POLICY "Open log access" ON public.logs FOR SELECT USING (true);
        """
        fp = self._write_file("003_open_logs.sql", content)
        violations = audit_supabase_file(fp)
        self.assertTrue(any(v["rule"] == "SUPABASE-PERMISSIVE-POLICY" for v in violations))

    def test_detects_client_service_key(self):
        content = 'const key = process.env.NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY;'
        fp = self._write_file("src/components/ClientAuth.tsx", content)
        violations = audit_supabase_file(fp)
        self.assertTrue(any(v["rule"] == "SUPABASE-EXPOSED-SERVICE-KEY" for v in violations))


if __name__ == "__main__":
    unittest.main()
