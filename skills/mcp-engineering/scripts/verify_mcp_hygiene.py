#!/usr/bin/env python3
"""
verify_mcp_hygiene.py - Audits MCP server and tool code for path-traversal and shell risks.
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, List

IGNORED_DIRS = {".git", "node_modules", "dist", "build", "__pycache__", "venv", ".venv"}
CHECKED_EXTS = {".ts", ".tsx", ".js", ".jsx", ".py"}


def audit_mcp_file(file_path: Path) -> List[Dict[str, str]]:
    """Inspect a source file for MCP path traversal, shell=True, or stdout JSON-RPC pollution."""
    issues: List[Dict[str, str]] = []
    content = file_path.read_text(encoding="utf-8", errors="ignore")
    is_mcp = any(
        tok in content
        for tok in ("McpServer", "StdioServerTransport", "CallToolRequest", "modelcontextprotocol", "stdioServer")
    )
    if not is_mcp:
        return issues

    if "shell=True" in content or "shell: true" in content:
        issues.append({"file": str(file_path), "rule": "MCP-UNSAFE-SHELL", "message": "MCP handler enables shell=True execution."})
    if re.search(r"\bpath\.join\([^)]*\)", content) and "realpath" not in content:
        issues.append({"file": str(file_path), "rule": "MCP-UNSANDBOXED-PATH", "message": "path.join() used in MCP server without realpath boundary verification."})
    if "StdioServerTransport" in content and "console.log(" in content:
        issues.append({"file": str(file_path), "rule": "MCP-STDIO-POLLUTION", "message": "console.log() corrupts stdio JSON-RPC frames; use console.error()."})
    return issues


def scan_directory(target_path: Path) -> List[Dict[str, str]]:
    """Scan file or directory for MCP hygiene violations."""
    if target_path.is_file():
        return audit_mcp_file(target_path)

    violations: List[Dict[str, str]] = []
    for root, dirs, files in os.walk(target_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for fname in sorted(files):
            if Path(fname).suffix.lower() in CHECKED_EXTS:
                violations.extend(audit_mcp_file(Path(root) / fname))
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit MCP server and tool hygiene.")
    parser.add_argument("--path", "-p", default=".", help="Path to inspect")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on findings")
    args = parser.parse_args()

    findings = scan_directory(Path(args.path).resolve())
    print(f"=== MCP Engineering Hygiene Audit: {args.path} ===")
    if not findings:
        print("[PASS] No MCP security or transport violations found.")
        return 0
    for f in findings:
        print(f"  - {f['file']} [{f['rule']}] {f['message']}")
    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
