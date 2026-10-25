#!/usr/bin/env python3
"""
Unit tests for validate_openapi_spec.py
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from validate_openapi_spec import validate_openapi_dict


class TestValidateOpenAPISpec(unittest.TestCase):
    def test_valid_spec_passes(self):
        spec = {
            "openapi": "3.1.0",
            "info": {"title": "Users API", "version": "1.0.0"},
            "paths": {
                "/v1/users": {
                    "get": {
                        "responses": {
                            "200": {"description": "List of users"},
                            "500": {"description": "Server error"}
                        }
                    }
                }
            }
        }
        violations = validate_openapi_dict(spec, "openapi.json")
        self.assertEqual(len(violations), 0)

    def test_detects_legacy_version(self):
        spec = {"openapi": "2.0", "paths": {}}
        violations = validate_openapi_dict(spec, "openapi.json")
        self.assertTrue(any(v["rule"] == "INVALID-OPENAPI-VERSION" for v in violations))

    def test_detects_missing_success_response(self):
        spec = {
            "openapi": "3.0.3",
            "paths": {
                "/v1/orders": {
                    "post": {
                        "responses": {
                            "400": {"description": "Validation error"}
                        }
                    }
                }
            }
        }
        violations = validate_openapi_dict(spec, "openapi.json")
        self.assertTrue(any(v["rule"] == "MISSING-SUCCESS-RESPONSE" for v in violations))


if __name__ == "__main__":
    unittest.main()
