#!/usr/bin/env python3
"""
verify_antigravity_hooks.py - Audits Antigravity Customization hooks.json files
for schema conformity, supported lifecycle events, matchers, timeouts, and script existence.

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder Antigravity Automation Engine
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

VALID_HOOK_EVENTS: Set[str] = {
    "SessionStart",
    "PreToolUse",
    "PostToolUse",
    "PreInvocation",
    "PostInvocation",
    "Stop"
}


def audit_hooks_file(hooks_path: Path, repo_root: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Audits hooks.json configuration."""
    violations: List[Dict[str, Any]] = []
    if not hooks_path.exists():
        return [{"rule": "FILE-NOT-FOUND", "message": f"Hooks file does not exist: {hooks_path}"}]

    try:
        data = json.loads(hooks_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [{"rule": "INVALID-JSON", "message": f"Malformed JSON in hooks file: {exc}"}]

    if not isinstance(data, dict):
        return [{"rule": "ROOT-NOT-OBJECT", "message": "Root of hooks.json must be a JSON object."}]

    base_dir = repo_root if repo_root else hooks_path.parent

    for hook_name, hook_spec in data.items():
        if not isinstance(hook_spec, dict):
            violations.append({
                "rule": "SPEC-NOT-OBJECT",
                "hook": hook_name,
                "message": f"Hook definition for '{hook_name}' must be an object."
            })
            continue

        for key, event_list in hook_spec.items():
            if key == "enabled":
                if not isinstance(event_list, bool):
                    violations.append({
                        "rule": "INVALID-ENABLED-TYPE",
                        "hook": hook_name,
                        "message": f"'enabled' field in '{hook_name}' must be a boolean."
                    })
                continue

            if key not in VALID_HOOK_EVENTS:
                violations.append({
                    "rule": "UNKNOWN-EVENT-TYPE",
                    "hook": hook_name,
                    "event": key,
                    "message": f"Unknown hook event '{key}' in '{hook_name}'. Supported events: {sorted(VALID_HOOK_EVENTS)}"
                })
                continue

            if not isinstance(event_list, list):
                violations.append({
                    "rule": "EVENT-NOT-LIST",
                    "hook": hook_name,
                    "event": key,
                    "message": f"Event definition for '{key}' in '{hook_name}' must be a list of handler configs."
                })
                continue

            for idx, handler in enumerate(event_list):
                if not isinstance(handler, dict):
                    violations.append({
                        "rule": "HANDLER-NOT-OBJECT",
                        "hook": hook_name,
                        "event": key,
                        "index": idx,
                        "message": f"Handler item {idx} in '{hook_name}.{key}' must be an object."
                    })
                    continue

                # Handler can have 'matcher' and 'hooks' list
                sub_hooks = handler.get("hooks", [])
                if not isinstance(sub_hooks, list):
                    violations.append({
                        "rule": "SUB-HOOKS-NOT-LIST",
                        "hook": hook_name,
                        "event": key,
                        "message": f"'hooks' list missing or not an array in handler {idx} of '{hook_name}.{key}'."
                    })
                    continue

                for h_idx, h_item in enumerate(sub_hooks):
                    if not isinstance(h_item, dict):
                        violations.append({
                            "rule": "HOOK-ITEM-NOT-OBJECT",
                            "hook": hook_name,
                            "event": key,
                            "message": f"Command item {h_idx} in '{hook_name}.{key}' must be an object."
                        })
                        continue

                    cmd = h_item.get("command")
                    if not cmd or not isinstance(cmd, str):
                        violations.append({
                            "rule": "MISSING-COMMAND",
                            "hook": hook_name,
                            "event": key,
                            "message": f"Hook item {h_idx} in '{hook_name}.{key}' missing valid 'command' string."
                        })
                        continue

                    timeout = h_item.get("timeout")
                    if timeout is not None and (not isinstance(timeout, (int, float)) or timeout <= 0):
                        violations.append({
                            "rule": "INVALID-TIMEOUT",
                            "hook": hook_name,
                            "event": key,
                            "message": f"Timeout in '{hook_name}.{key}' must be a positive number."
                        })

                    # Check script reference if command references a local file
                    words = cmd.split()
                    for word in words:
                        if word.endswith(".py") or word.endswith(".sh"):
                            script_candidate = base_dir / word
                            if not script_candidate.exists():
                                violations.append({
                                    "rule": "SCRIPT-FILE-NOT-FOUND",
                                    "hook": hook_name,
                                    "script": word,
                                    "message": f"Referenced hook script does not exist: {script_candidate}"
                                })

    return violations


def main() -> None:
    parser = argparse.ArgumentParser(description="Antigravity Hooks Validator")
    parser.add_argument("path", type=Path, help="Path to hooks.json")
    parser.add_argument("--repo-root", type=Path, help="Optional repo root to resolve relative scripts")
    args = parser.parse_args()

    violations = audit_hooks_file(args.path, args.repo_root)
    if violations:
        print(f"[FAIL] Found {len(violations)} hooks.json issue(s):", file=sys.stderr)
        for v in violations:
            print(f"  • [{v.get('rule')}] {v.get('message')}", file=sys.stderr)
        sys.exit(1)

    print(f"[PASS] All hooks in {args.path} conform to Antigravity specifications.")


if __name__ == "__main__":
    main()
