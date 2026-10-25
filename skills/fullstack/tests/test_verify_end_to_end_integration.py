#!/usr/bin/env python3
"""
Unit tests for verify_end_to_end_integration.py
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from verify_end_to_end_integration import audit_route_file


class TestVerifyEndToEndIntegration(unittest.TestCase):
    def test_clean_route_passes(self):
        code = """
        import { z } from 'zod';
        import { db } from '@/lib/db';

        const CreateUserSchema = z.object({ name: z.string() });

        export async function POST(req: Request) {
            const body = await req.json();
            const valid = CreateUserSchema.parse(body);
            const user = await db.users.create({ data: valid });
            return Response.json(user, { status: 201 });
        }
        """
        violations = audit_route_file("src/app/api/users/route.ts", code)
        self.assertEqual(len(violations), 0)

    def test_detects_mock_toggle_flag(self):
        code = "const isMockMode = true;\nexport const data = [];"
        violations = audit_route_file("service.ts", code)
        self.assertTrue(any(v["rule"] == "MOCK-TOGGLE-FLAG-DETECTED" for v in violations))

    def test_detects_missing_persistence_in_route(self):
        code = """
        import { z } from 'zod';
        export async function POST(req: Request) {
            const body = await req.json();
            return Response.json({ success: true });
        }
        """
        violations = audit_route_file("routes/controller.ts", code)
        self.assertTrue(any(v["rule"] == "MISSING-REAL-PERSISTENCE" for v in violations))

    def test_detects_missing_schema_validation(self):
        code = """
        import { db } from '@/db';
        export async function POST(req: Request) {
            const body = await req.json();
            const res = await db.users.insert(body);
            return Response.json(res);
        }
        """
        violations = audit_route_file("api/users/route.ts", code)
        self.assertTrue(any(v["rule"] == "MISSING-SCHEMA-VALIDATION" for v in violations))


if __name__ == "__main__":
    unittest.main()
