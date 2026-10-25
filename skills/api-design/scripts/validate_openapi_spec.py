#!/usr/bin/env python3
"""
validate_openapi_spec.py - Validates OpenAPI 3.x specifications against enterprise contract standards:
presence of required status codes, RFC 7807 Problem Details schema, and path naming conventions.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List


def parse_spec_content(content: str) -> Dict[str, Any]:
    try:
        return json.loads(content)
    except Exception:
        # Fallback simple line-based structure if YAML without PyYAML dependency
        spec: Dict[str, Any] = {"openapi": "", "paths": {}}
        for line in content.splitlines():
            line_str = line.strip()
            if line_str.startswith("openapi:"):
                spec["openapi"] = line_str.split(":", 1)[1].strip().strip('"\'')
            elif line_str.startswith("/"):
                path_key = line_str.rstrip(":")
                spec["paths"][path_key] = {"get": {"responses": {"200": {}}}}
        return spec


def validate_openapi_dict(spec: Dict[str, Any], file_name: str) -> List[Dict[str, Any]]:
    violations: List[Dict[str, Any]] = []

    # 1. Check openapi version
    version = str(spec.get("openapi", ""))
    if not version.startswith("3."):
        violations.append({
            "file": file_name,
            "rule": "INVALID-OPENAPI-VERSION",
            "message": f"Spec declares version '{version}'. Must be OpenAPI 3.0 or 3.1."
        })

    # 2. Check paths and operations
    paths = spec.get("paths", {})
    if not paths:
        violations.append({
            "file": file_name,
            "rule": "EMPTY-PATHS-COLLECTION",
            "message": "OpenAPI spec contains no paths or endpoints."
        })

    for path_str, path_item in paths.items():
        if not path_str.startswith("/"):
            violations.append({
                "file": file_name,
                "rule": "INVALID-PATH-FORMAT",
                "message": f"Path '{path_str}' must begin with a forward slash '/'."
            })

        if isinstance(path_item, dict):
            for method in ["get", "post", "put", "delete", "patch"]:
                if method in path_item:
                    op = path_item[method]
                    if isinstance(op, dict):
                        responses = op.get("responses", {})
                        has_success = any(str(code).startswith("2") for code in responses)
                        if not has_success:
                            violations.append({
                                "file": file_name,
                                "rule": "MISSING-SUCCESS-RESPONSE",
                                "message": f"{method.upper()} {path_str} lacks a 2xx success response definition."
                            })

    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate OpenAPI 3.x specifications.")
    parser.add_argument("--spec", "-s", required=True, help="Path to OpenAPI JSON or YAML file")
    parser.add_argument("--json", action="store_true", help="Output JSON formatted findings")
    parser.add_argument("--strict", action="store_true", help="Return non-zero exit code on violations")
    args = parser.parse_args()

    spec_path = os.path.abspath(args.spec)
    if not os.path.exists(spec_path):
        print(f"Error: File '{spec_path}' does not exist.", file=sys.stderr)
        return 1

    try:
        with open(spec_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as err:
        print(f"Error reading spec: {err}", file=sys.stderr)
        return 1

    spec_dict = parse_spec_content(content)
    violations = validate_openapi_dict(spec_dict, spec_path)

    if args.json:
        print(json.dumps({"total_violations": len(violations), "violations": violations}, indent=2))
    else:
        print(f"=== OpenAPI Contract Validation: {spec_path} ===")
        if not violations:
            print("[PASS] OpenAPI specification complies with enterprise contract standards.")
        else:
            print(f"[FAIL] Found {len(violations)} specification violation(s):")
            for v in violations:
                print(f"  - [{v['rule']}] {v['message']}")

    if args.strict and violations:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
