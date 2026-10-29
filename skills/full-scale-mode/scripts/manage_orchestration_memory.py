#!/usr/bin/env python3
"""
manage_orchestration_memory.py - Orchestration Memory Management Engine.

Manages deterministic, structured execution state for Full-Scale Mode:
.agents/memory/orchestration_state.json

Author: Arron Kian Parejas (@darknecrocities)
Part of SkillBuilder Full-Scale Mode Engine
"""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional

DEFAULT_MEMORY_RELATIVE_PATH = Path(".agents") / "memory" / "orchestration_state.json"
VALID_STAGES = ["DISCOVER", "PLAN", "BUILD", "VERIFY", "LOOP", "RELEASE"]
VALID_TRIAD_PHASES = ["PHASE_1_FRONTEND", "PHASE_2_BACKEND", "PHASE_3_TESTING", "COMPLETED"]
STAGE_ORDER = ["DISCOVER", "PLAN", "BUILD", "VERIFY", "RELEASE"]

DEFAULT_MILESTONES = [
    {"id": "M-DISCOVER", "title": "Stage 1: Discover & Memory Recall", "status": "PENDING", "completed_at": None},
    {"id": "M-PLAN", "title": "Stage 2: Plan & Architectural Blueprint", "status": "PENDING", "completed_at": None},
    {"id": "M-BUILD", "title": "Stage 3: Build & Atomic Execution", "status": "PENDING", "completed_at": None},
    {"id": "M-VERIFY", "title": "Stage 4: Verify & Harness Evaluation", "status": "PENDING", "completed_at": None},
    {"id": "M-RELEASE", "title": "Stage 5: Release & Memory Consolidation", "status": "PENDING", "completed_at": None},
]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def resolve_memory_file(repo_root: Optional[Path] = None, custom_file: Optional[str] = None) -> Path:
    if custom_file:
        return Path(custom_file).resolve()
    base = repo_root if repo_root else Path.cwd()
    return (base / DEFAULT_MEMORY_RELATIVE_PATH).resolve()


def create_initial_state(
    session_id: str,
    goal: str = "",
    platform: str = "auto"
) -> Dict[str, Any]:
    now = utc_now_iso()
    return {
        "version": "1.0.0",
        "session_id": session_id,
        "goal": goal,
        "timestamp_started": now,
        "timestamp_updated": now,
        "current_stage": "DISCOVER",
        "triad_phase": "PHASE_1_FRONTEND",
        "platform_target": platform,
        "milestones": list(DEFAULT_MILESTONES),
        "file_registry": {"created": [], "modified": []},
        "backup_digest": None,
        "harness_history": [],
        "invariants_learned": [],
        "token_usage_estimate": 0,
    }


def load_memory(memory_path: Path) -> Optional[Dict[str, Any]]:
    if not memory_path.exists():
        return None
    try:
        content = memory_path.read_text(encoding="utf-8")
        return json.loads(content)
    except (json.JSONDecodeError, OSError):
        return None


def save_memory(memory_path: Path, data: Dict[str, Any]) -> None:
    data["timestamp_updated"] = utc_now_iso()
    memory_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = memory_path.with_suffix(".tmp")
    temp_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    temp_path.replace(memory_path)


def init_memory(memory_path: Path, session_id: str, goal: str, platform: str) -> Dict[str, Any]:
    state = create_initial_state(session_id, goal=goal, platform=platform)
    save_memory(memory_path, state)
    return state


def update_checkpoint(
    data: Dict[str, Any],
    stage: Optional[str] = None,
    triad_phase: Optional[str] = None,
    backup_digest: Optional[str] = None,
    created_file: Optional[str] = None,
    modified_file: Optional[str] = None,
    token_delta: int = 0
) -> Dict[str, Any]:
    if stage:
        if stage not in VALID_STAGES:
            raise ValueError(f"Invalid stage '{stage}'. Must be one of: {VALID_STAGES}")
        data["current_stage"] = stage
    if triad_phase:
        if triad_phase not in VALID_TRIAD_PHASES:
            raise ValueError(f"Invalid phase '{triad_phase}'. Must be one of: {VALID_TRIAD_PHASES}")
        data["triad_phase"] = triad_phase
    if backup_digest:
        data["backup_digest"] = backup_digest
    if created_file and created_file not in data["file_registry"]["created"]:
        data["file_registry"]["created"].append(created_file)
    if modified_file and modified_file not in data["file_registry"]["modified"]:
        data["file_registry"]["modified"].append(modified_file)
    if token_delta > 0:
        data["token_usage_estimate"] = data.get("token_usage_estimate", 0) + token_delta
    return data


def record_milestone_completion(data: Dict[str, Any], milestone_id: str, status: str = "COMPLETED") -> bool:
    found = False
    for m in data.get("milestones", []):
        if m["id"].upper() == milestone_id.upper():
            m["status"] = status
            m["completed_at"] = utc_now_iso() if status == "COMPLETED" else None
            found = True
            break
    if not found:
        data.setdefault("milestones", []).append({
            "id": milestone_id,
            "title": f"Custom Milestone: {milestone_id}",
            "status": status,
            "completed_at": utc_now_iso() if status == "COMPLETED" else None,
        })
    return True


def record_harness_iteration(
    data: Dict[str, Any],
    iteration: int,
    passed: bool,
    failing_tiers: List[str],
    failure_count: int
) -> None:
    entry = {
        "iteration": iteration,
        "timestamp": utc_now_iso(),
        "passed": passed,
        "failing_tiers": failing_tiers,
        "failure_count": failure_count,
    }
    data.setdefault("harness_history", []).append(entry)


def advance_stage_transition(data: Dict[str, Any]) -> str:
    current = data.get("current_stage", "DISCOVER")
    if current == "LOOP":
        data["current_stage"] = "VERIFY"
        return "VERIFY"
    if current not in STAGE_ORDER:
        data["current_stage"] = "DISCOVER"
        return "DISCOVER"
    idx = STAGE_ORDER.index(current)
    if idx + 1 < len(STAGE_ORDER):
        next_stage = STAGE_ORDER[idx + 1]
        data["current_stage"] = next_stage
        return next_stage
    return current


def format_status_summary(data: Dict[str, Any], path: Path) -> str:
    lines = [
        f"=== Orchestration Memory State ({path.name}) ===",
        f"Session ID     : {data.get('session_id', 'N/A')}",
        f"Goal           : {data.get('goal', 'N/A')}",
        f"Current Stage  : [{data.get('current_stage', 'UNKNOWN')}]",
        f"Triad Phase    : [{data.get('triad_phase', 'UNKNOWN')}]",
        f"Platform Target: [{data.get('platform_target', 'AUTO').upper()}]",
        f"Files Tracked  : {len(data.get('file_registry', {}).get('created', []))} created, "
        f"{len(data.get('file_registry', {}).get('modified', []))} modified",
        f"Backup Digest  : {data.get('backup_digest') or 'None'}",
        f"Harness Runs   : {len(data.get('harness_history', []))} run(s)",
        "Milestones:",
    ]
    for m in data.get("milestones", []):
        mark = "✓" if m.get("status") == "COMPLETED" else "○"
        lines.append(f"  [{mark}] {m.get('id')}: {m.get('title')} ({m.get('status')})")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Orchestration Memory Subsystem CLI")
    p.add_argument("--file", "-f", help="Custom path to orchestration_state.json")
    p.add_argument("--repo-root", "-r", help="Repository root directory")
    sub = p.add_subparsers(dest="command", required=True)

    init_cmd = sub.add_parser("init", help="Initialize active session memory")
    init_cmd.add_argument("--session-id", "-s", default="session-001", help="Unique session ID")
    init_cmd.add_argument("--goal", "-g", default="", help="Goal or prompt description")
    init_cmd.add_argument("--platform", "-p", default="auto", choices=["auto", "mobile", "web", "universal"])

    sub.add_parser("status", help="Display memory status summary")
    sub.add_parser("dump", help="Dump raw JSON memory state")
    sub.add_parser("advance", help="Advance to the next lifecycle stage")

    cp_cmd = sub.add_parser("checkpoint", help="Update execution checkpoints")
    cp_cmd.add_argument("--stage", choices=VALID_STAGES, help="Update active stage")
    cp_cmd.add_argument("--phase", choices=VALID_TRIAD_PHASES, help="Update triad phase")
    cp_cmd.add_argument("--backup", help="Set SHA-256 backup digest")
    cp_cmd.add_argument("--created", help="Register a created file path")
    cp_cmd.add_argument("--modified", help="Register a modified file path")
    cp_cmd.add_argument("--tokens", type=int, default=0, help="Record estimated tokens consumed")

    ms_cmd = sub.add_parser("milestone", help="Record milestone progress")
    ms_cmd.add_argument("--id", required=True, help="Milestone ID (e.g. M-DISCOVER)")
    ms_cmd.add_argument("--status", default="COMPLETED", choices=["COMPLETED", "IN_PROGRESS", "PENDING"])

    hr_cmd = sub.add_parser("record-harness", help="Log a harness execution result")
    hr_cmd.add_argument("--iteration", type=int, required=True, help="Loop iteration number")
    hr_cmd.add_argument("--passed", action="store_true", help="Set if harness passed")
    hr_cmd.add_argument("--tier", action="append", default=[], help="Failing tier name(s)")
    hr_cmd.add_argument("--failures", type=int, default=0, help="Failure count")

    sub.add_parser("clear", help="Remove or reset active memory state")
    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    root = Path(args.repo_root).resolve() if args.repo_root else None
    mem_path = resolve_memory_file(repo_root=root, custom_file=args.file)

    if args.command == "init":
        state = init_memory(mem_path, session_id=args.session_id, goal=args.goal, platform=args.platform)
        print(f"[OK] Initialized orchestration memory at: {mem_path}")
        return 0

    state = load_memory(mem_path)
    if state is None and args.command != "clear":
        print(f"[ERROR] Memory state file not found at: {mem_path}. Run 'init' first.", file=sys.stderr)
        return 1

    if args.command == "status":
        print(format_status_summary(state, mem_path))
        return 0
    elif args.command == "dump":
        print(json.dumps(state, indent=2))
        return 0
    elif args.command == "advance":
        next_s = advance_stage_transition(state)
        save_memory(mem_path, state)
        print(f"[OK] Advanced stage to: {next_s}")
        return 0
    elif args.command == "checkpoint":
        state = update_checkpoint(
            state, stage=args.stage, triad_phase=args.phase, backup_digest=args.backup,
            created_file=args.created, modified_file=args.modified, token_delta=args.tokens
        )
        save_memory(mem_path, state)
        print(f"[OK] Checkpointed stage [{state['current_stage']}] and phase [{state['triad_phase']}].")
        return 0
    elif args.command == "milestone":
        record_milestone_completion(state, milestone_id=args.id, status=args.status)
        save_memory(mem_path, state)
        print(f"[OK] Milestone '{args.id}' updated to {args.status}.")
        return 0
    elif args.command == "record-harness":
        record_harness_iteration(
            state, iteration=args.iteration, passed=args.passed,
            failing_tiers=args.tier, failure_count=args.failures
        )
        save_memory(mem_path, state)
        print(f"[OK] Harness iteration {args.iteration} logged (Passed: {args.passed}).")
        return 0
    elif args.command == "clear":
        if mem_path.exists():
            mem_path.unlink()
            print(f"[OK] Cleared memory state at: {mem_path}")
        else:
            print(f"[INFO] No memory state found to clear at: {mem_path}")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
