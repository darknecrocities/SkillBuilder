#!/usr/bin/env python3
"""Unit tests for mcp-engineering hygiene auditor."""

import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import verify_mcp_hygiene  # noqa: E402


class TestVerifyMcpHygiene(unittest.TestCase):
    def test_detects_unsandboxed_path_and_stdio_pollution(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "server.ts"
            bad.write_text(
                'import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";\n'
                'console.log("starting");\n'
                'const target = path.join(root, args.file);\n',
                encoding="utf-8",
            )
            issues = verify_mcp_hygiene.scan_directory(bad)
            rules = {i["rule"] for i in issues}
            self.assertIn("MCP-STDIO-POLLUTION", rules)
            self.assertIn("MCP-UNSANDBOXED-PATH", rules)

    def test_clean_sandboxed_server_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            good = Path(tmp) / "server.ts"
            good.write_text(
                'import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";\n'
                'console.error("starting");\n'
                'const real = fs.realpathSync(path.resolve(root, args.file));\n',
                encoding="utf-8",
            )
            issues = verify_mcp_hygiene.scan_directory(good)
            self.assertEqual(issues, [])


if __name__ == "__main__":
    unittest.main()
