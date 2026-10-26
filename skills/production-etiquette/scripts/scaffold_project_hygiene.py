#!/usr/bin/env python3
"""
scaffold_project_hygiene.py - Audits and scaffolds production hygiene files.

Checks and scaffolds:
1. .gitignore (complete with secret & artifact exclusions)
2. .env.example (configuration contract)
3. Dockerfile (multi-stage, non-root)
4. .dockerignore
5. docker-compose.yml (with health checks)
6. .github/workflows/ci.yml (CI/CD pipeline)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"

DEFAULT_GITIGNORE = """# Environment & Secrets (NEVER COMMIT)
.env
.env.*
!.env.example
*.key
*.pem
*.cert
*.crt
id_rsa
secrets/

# Dependencies
node_modules/
vendor/
venv/
.venv/
__pycache__/
*.pyc

# Build & Distribution Artifacts
dist/
build/
out/
.next/
.nuxt/
target/
*.egg-info/

# Logs & Diagnostics
*.log
npm-debug.log*
yarn-debug.log*
coverage/
.nyc_output/

# Operating System & IDE Files
.DS_Store
Thumbs.db
.idea/
.vscode/
*.swp
*.swo
"""

DEFAULT_ENV_EXAMPLE = """# Server Configuration
PORT=3000
NODE_ENV=development
LOG_LEVEL=info

# Database Connection (PostgreSQL)
DATABASE_URL=postgres://appuser:apppassword@localhost:5432/appdb
POSTGRES_DB=appdb
POSTGRES_USER=appuser
POSTGRES_PASSWORD=apppassword

# Authentication & Security
# Generate a 32-character secret: openssl rand -base64 32
JWT_SECRET=your_jwt_secret_min_32_characters_here
JWT_EXPIRES_IN=15m

# External Integrations (Replace with test/sandbox credentials)
API_TIMEOUT_MS=5000
EXTERNAL_SERVICE_API_KEY=placeholder_api_key_here
"""

DEFAULT_DOCKERIGNORE = """# Source Control & IDEs
.git
.gitignore
.idea
.vscode
*.swp

# Environment & Secrets
.env
.env.*
!.env.example

# Local Dependencies
node_modules
vendor
venv
.venv
__pycache__

# Build Outputs & Tests
dist
build
coverage
*.log
.DS_Store

# Docker & CI files
Dockerfile*
docker-compose*.yml
.github
"""


def detect_ecosystem(target_dir: Path) -> str:
    """Detect the primary programming language/ecosystem."""
    if (target_dir / "package.json").exists():
        return "node"
    if (target_dir / "requirements.txt").exists() or (target_dir / "pyproject.toml").exists():
        return "python"
    if (target_dir / "go.mod").exists():
        return "go"
    return "generic"


def get_template_content(relative_path: str, fallback_content: str) -> str:
    """Read template file if available, otherwise return fallback string."""
    candidate = TEMPLATE_DIR / relative_path
    if candidate.exists():
        try:
            return candidate.read_text(encoding="utf-8")
        except OSError:
            return fallback_content
    return fallback_content


def get_dockerfile_template(ecosystem: str) -> str:
    if ecosystem == "python":
        return get_template_content("docker/Dockerfile.python", "# Python Dockerfile\n")
    if ecosystem == "go":
        return get_template_content("docker/Dockerfile.go", "# Go Dockerfile\n")
    return get_template_content("docker/Dockerfile.node", "# Node Dockerfile\n")


def audit_project(target_dir: Path) -> Dict[str, bool]:
    """Check existence of all 7 mandatory hygiene files."""
    return {
        ".gitignore": (target_dir / ".gitignore").exists(),
        ".env.example": (target_dir / ".env.example").exists(),
        "Dockerfile": (target_dir / "Dockerfile").exists(),
        ".dockerignore": (target_dir / ".dockerignore").exists(),
        "docker-compose.yml": (target_dir / "docker-compose.yml").exists(),
        ".github/workflows/ci.yml": (target_dir / ".github" / "workflows" / "ci.yml").exists(),
        ".github/pull_request_template.md": (target_dir / ".github" / "pull_request_template.md").exists(),
    }


def apply_hygiene(target_dir: Path, ecosystem: str) -> List[str]:
    """Scaffold missing hygiene files without overwriting existing files."""
    created_files: List[str] = []

    files_to_create = [
        (".gitignore", DEFAULT_GITIGNORE),
        (".env.example", DEFAULT_ENV_EXAMPLE),
        ("Dockerfile", get_dockerfile_template(ecosystem)),
        (".dockerignore", DEFAULT_DOCKERIGNORE),
        ("docker-compose.yml", get_template_content("docker/docker-compose.yml", "services:\n")),
        (".github/workflows/ci.yml", get_template_content("ci-cd/github-ci.yml", "name: CI\n")),
        (".github/pull_request_template.md", get_template_content("ci-cd/pull_request_template.md", "## Summary\n")),
    ]

    for rel_path, content in files_to_create:
        dest_file = target_dir / rel_path
        if not dest_file.exists():
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            dest_file.write_text(content, encoding="utf-8")
            created_files.append(rel_path)

    return created_files


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audit and scaffold production project hygiene files."
    )
    parser.add_argument(
        "--path", "-p",
        type=str,
        default=".",
        help="Path to project root directory.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Audit project and report missing hygiene files without modifying.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Scaffold missing hygiene files automatically.",
    )
    parser.add_argument(
        "--type", "-t",
        choices=["auto", "node", "python", "go", "generic"],
        default="auto",
        help="Ecosystem type for templates.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    target_dir = Path(args.path).resolve()
    if not target_dir.exists() or not target_dir.is_dir():
        sys.stderr.write(f"Error: Path '{args.path}' does not exist or is not a directory.\n")
        return 2

    ecosystem = detect_ecosystem(target_dir) if args.type == "auto" else args.type
    audit_results = audit_project(target_dir)
    missing = [f for f, exists in audit_results.items() if not exists]

    created: List[str] = []
    if args.apply:
        created = apply_hygiene(target_dir, ecosystem)
        # Refresh audit
        audit_results = audit_project(target_dir)
        missing = [f for f, exists in audit_results.items() if not exists]

    if args.json:
        payload = {
            "project_path": str(target_dir),
            "ecosystem": ecosystem,
            "status": "pass" if not missing else "fail",
            "audit": audit_results,
            "missing_count": len(missing),
            "missing_files": missing,
            "created_files": created,
        }
        print(json.dumps(payload, indent=2))
    else:
        print(f"\nProject Hygiene Audit (Ecosystem: {ecosystem})")
        print(f"Target: {target_dir}\n")

        for f, exists in audit_results.items():
            status = "[OK]    " if exists else "[MISSING]"
            print(f"  {status} {f}")

        if created:
            print(f"\n[APPLIED] Successfully scaffolded {len(created)} file(s):")
            for c in created:
                print(f"  + Created {c}")

        if missing and not args.apply:
            print(f"\n[FAIL] Found {len(missing)} missing production hygiene item(s).")
            print("Run with `--apply` to automatically scaffold missing files.")
            return 1
        elif not missing:
            print("\n[PASS] All production hygiene standards are satisfied.")

    return 1 if (missing and not args.apply) else 0


if __name__ == "__main__":
    sys.exit(main())
