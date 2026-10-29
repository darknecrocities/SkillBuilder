#!/usr/bin/env python3
"""
generate_sidecar_automation.py - Generates, validates, and deploys Google Antigravity
scheduled sidecars (~/.gemini/jetski/sidecars/<slug>/sidecar.json).

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder Antigravity Automation Engine
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

CRON_REGEX = re.compile(
    r"^(\*|[0-5]?\d)(/\d+)?(\s+(\*|[01]?\d|2[0-3])(/\d+)?){1}(\s+(\*|[0-2]?\d|3[01])(/\d+)?){1}"
    r"(\s+(\*|[01]?\d)(/\d+)?){1}(\s+(\*|[0-6])(/\d+)?){1}$"
)

DEFAULT_SIDECARS_DIR = Path.home() / ".gemini" / "jetski" / "sidecars"


def validate_cron_expression(cron_expr: str) -> Tuple[bool, str]:
    """Validates a standard 5-field cron expression."""
    fields = cron_expr.strip().split()
    if len(fields) != 5:
        return False, f"Cron expression must contain exactly 5 fields, got {len(fields)}: '{cron_expr}'"
    return True, "Valid cron expression"


def validate_timezone(tz: str) -> Tuple[bool, str]:
    """Validates that a timezone string follows IANA naming conventions."""
    if not tz or "/" not in tz and tz.upper() != "UTC":
        return False, f"Timezone must be an IANA identifier (e.g. 'America/New_York', 'UTC'), got '{tz}'"
    return True, "Valid IANA timezone"


def build_sidecar_payload(cron_expr: str, timezone: str, prompt: str) -> Dict[str, Any]:
    """Constructs the canonical Antigravity scheduled sidecar JSON dictionary."""
    is_cron_valid, cron_err = validate_cron_expression(cron_expr)
    if not is_cron_valid:
        raise ValueError(cron_err)

    is_tz_valid, tz_err = validate_timezone(timezone)
    if not is_tz_valid:
        raise ValueError(tz_err)

    if not prompt.strip():
        raise ValueError("Prompt must not be empty.")

    formatted_schedule = f"CRON_TZ={timezone} {cron_expr.strip()}"
    return {
        "builtin": "schedule",
        "args": {
            "schedule": formatted_schedule,
            "prompt": prompt.strip()
        }
    }


def deploy_sidecar(
    slug: str,
    cron_expr: str,
    timezone: str,
    prompt: str,
    output_dir: Optional[Path] = None,
    dry_run: bool = False
) -> Tuple[Path, Dict[str, Any]]:
    """Creates sidecar.json in target directory."""
    clean_slug = re.sub(r"[^a-zA-Z0-9_-]", "-", slug.lower().strip())
    if not clean_slug:
        raise ValueError("Slug cannot be empty.")

    payload = build_sidecar_payload(cron_expr, timezone, prompt)
    base_dir = output_dir if output_dir else DEFAULT_SIDECARS_DIR
    target_dir = base_dir / clean_slug
    target_file = target_dir / "sidecar.json"

    if dry_run:
        return target_file, payload

    target_dir.mkdir(parents=True, exist_ok=True)
    target_file.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return target_file, payload


def list_existing_sidecars(base_dir: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Discovers and inspects existing scheduled sidecars."""
    search_dir = base_dir if base_dir else DEFAULT_SIDECARS_DIR
    results: List[Dict[str, Any]] = []
    if not search_dir.exists():
        return results

    for child in sorted(search_dir.iterdir()):
        if child.is_dir():
            sidecar_path = child / "sidecar.json"
            if sidecar_path.exists():
                try:
                    data = json.loads(sidecar_path.read_text(encoding="utf-8"))
                    results.append({
                        "slug": child.name,
                        "path": str(sidecar_path),
                        "builtin": data.get("builtin", "unknown"),
                        "schedule": data.get("args", {}).get("schedule", ""),
                        "prompt": data.get("args", {}).get("prompt", "")[:80] + "..."
                    })
                except Exception as exc:
                    results.append({"slug": child.name, "error": str(exc)})
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Antigravity Scheduled Sidecar Generator")
    parser.add_argument("--slug", help="Slug name for the sidecar automation")
    parser.add_argument("--cron", help="Standard 5-field cron expression (e.g. '0 9 * * 1-5')")
    parser.add_argument("--timezone", default="UTC", help="IANA timezone (e.g. 'America/New_York', default 'UTC')")
    parser.add_argument("--prompt", help="Self-contained execution prompt for the agent")
    parser.add_argument("--output-dir", type=Path, help="Custom output directory")
    parser.add_argument("--dry-run", action="store_true", help="Print generated JSON without writing to disk")
    parser.add_argument("--list", action="store_true", help="List active Antigravity sidecars")

    args = parser.parse_args()

    if args.list:
        sidecars = list_existing_sidecars(args.output_dir)
        print(f"Found {len(sidecars)} Antigravity sidecars:")
        for sc in sidecars:
            print(f"  • {sc.get('slug')}: {sc.get('schedule', 'no-schedule')} -> {sc.get('path', '')}")
        return

    if not args.slug or not args.cron or not args.prompt:
        parser.error("--slug, --cron, and --prompt are required unless --list is specified.")

    try:
        path, payload = deploy_sidecar(
            slug=args.slug,
            cron_expr=args.cron,
            timezone=args.timezone,
            prompt=args.prompt,
            output_dir=args.output_dir,
            dry_run=args.dry_run
        )
        if args.dry_run:
            print("[DRY-RUN] Target Path:", path)
            print(json.dumps(payload, indent=2))
        else:
            print(f"[SUCCESS] Antigravity Sidecar created at: {path}")
            print(json.dumps(payload, indent=2))
    except Exception as exc:
        print(f"[ERROR] Failed to deploy sidecar: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
