#!/usr/bin/env python3
"""
schedule_in_turn_helper.py - Helper utility to validate, parse, and construct
payloads for Antigravity's in-session 'schedule' tool, handling one-shot timers,
recurring crons, and TimerCondition settings.

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder Antigravity Automation Engine
"""

import argparse
import json
import sys
from typing import Any, Dict, Optional, Tuple


def build_in_turn_timer(
    prompt: str,
    duration_seconds: int,
    timer_condition: str = "never"
) -> Dict[str, Any]:
    """Builds arguments for a one-shot timer schedule call."""
    if duration_seconds <= 0:
        raise ValueError(f"duration_seconds must be positive, got {duration_seconds}")

    valid_conditions = {"never", "any"}
    if timer_condition not in valid_conditions and not timer_condition.startswith("agent-") and not timer_condition.startswith("subagent-"):
        # Could also be an arbitrary conversation ID
        pass

    if not prompt.strip():
        raise ValueError("Prompt must not be empty.")

    return {
        "DurationSeconds": duration_seconds,
        "Prompt": prompt.strip(),
        "TimerCondition": timer_condition
    }


def build_in_turn_cron(
    prompt: str,
    cron_expr: str,
    max_iterations: Optional[int] = None,
    is_daemon: bool = False
) -> Dict[str, Any]:
    """Builds arguments for a recurring cron schedule call."""
    fields = cron_expr.strip().split()
    if len(fields) != 5:
        raise ValueError(f"Cron expression must contain exactly 5 fields, got {len(fields)}: '{cron_expr}'")

    if not prompt.strip():
        raise ValueError("Prompt must not be empty.")

    payload: Dict[str, Any] = {
        "CronExpression": cron_expr.strip(),
        "Prompt": prompt.strip(),
    }

    if max_iterations is not None:
        if max_iterations <= 0:
            raise ValueError(f"max_iterations must be positive, got {max_iterations}")
        payload["MaxIterations"] = max_iterations

    if is_daemon:
        payload["IsDaemon"] = True

    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Antigravity In-Turn Schedule Helper")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    # Timer mode
    timer_parser = subparsers.add_parser("timer", help="Create a one-shot timer payload")
    timer_parser.add_argument("--seconds", type=int, required=True, help="Timer duration in seconds")
    timer_parser.add_argument("--prompt", required=True, help="Wakeup prompt")
    timer_parser.add_argument("--condition", default="never", help="TimerCondition ('never', 'any', or sender id)")

    # Cron mode
    cron_parser = subparsers.add_parser("cron", help="Create a recurring cron payload")
    cron_parser.add_argument("--cron", required=True, help="5-field cron expression (e.g. '*/5 * * * *')")
    cron_parser.add_argument("--prompt", required=True, help="Wakeup prompt")
    cron_parser.add_argument("--max-iterations", type=int, help="Optional max iterations")
    cron_parser.add_argument("--daemon", action="store_true", help="Set IsDaemon=True for standing jobs")

    args = parser.parse_args()

    try:
        if args.mode == "timer":
            payload = build_in_turn_timer(args.prompt, args.seconds, args.condition)
        else:
            payload = build_in_turn_cron(args.prompt, args.cron, args.max_iterations, args.daemon)
        print(json.dumps(payload, indent=2))
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
