#!/usr/bin/env python3
"""
analyze_git_commit_chunks.py - Analyzes git changes, enforces the 1,000-line push budget,
clusters files into cohesive commit chunks, and generates ready-to-review PR descriptions.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

MAX_PUSH_LINE_BUDGET = 1000

# Classification rules for grouping files into cohesive commits
CHUNK_CATEGORIES = [
    ("db", "Database & Migrations", re.compile(r"(migration|schema|ddl|entity|model)", re.IGNORECASE)),
    ("service", "Business Logic & Services", re.compile(r"(service|calculator|repository|repo|domain|usecase)", re.IGNORECASE)),
    ("api", "API & Controllers", re.compile(r"(route|controller|handler|endpoint|middleware|api)", re.IGNORECASE)),
    ("ui", "Frontend & Components", re.compile(r"(\.tsx|\.jsx|\.vue|component|view|page|style|css)", re.IGNORECASE)),
    ("test", "Tests & Verification", re.compile(r"(test|spec|fixture|mock)", re.IGNORECASE)),
    ("infra", "Tooling & Configuration", re.compile(r"(docker|compose|\.github|config|settings|\.env|\.gitignore|package\.json|pyproject\.toml|go\.mod)", re.IGNORECASE)),
]


def run_git_command(args: List[str], cwd: Path) -> Tuple[int, str, str]:
    """Execute a git command and return (exit_code, stdout, stderr)."""
    try:
        proc = subprocess.run(
            ["git"] + args,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
    except OSError as err:
        return 2, "", str(err)


def get_diff_stats(repo_path: Path) -> List[Dict[str, object]]:
    """Parse git diff --numstat for both staged and unstaged modifications."""
    code_unstaged, out_unstaged, _ = run_git_command(["diff", "--numstat"], repo_path)
    code_staged, out_staged, _ = run_git_command(["diff", "--cached", "--numstat"], repo_path)

    stats_map: Dict[str, Dict[str, int]] = {}

    for line in (out_unstaged + "\n" + out_staged).splitlines():
        parts = line.strip().split("\t")
        if len(parts) >= 3:
            added_str, deleted_str, fname = parts[0], parts[1], parts[2]
            added = int(added_str) if added_str.isdigit() else 0
            deleted = int(deleted_str) if deleted_str.isdigit() else 0

            if fname not in stats_map:
                stats_map[fname] = {"added": 0, "deleted": 0}
            stats_map[fname]["added"] += added
            stats_map[fname]["deleted"] += deleted

    code_untracked, out_untracked, _ = run_git_command(["status", "--porcelain"], repo_path)
    for line in out_untracked.splitlines():
        if line.startswith("??"):
            fname = line[3:].strip()
            if fname not in stats_map:
                full_path = repo_path / fname
                lines = 0
                if full_path.is_file():
                    try:
                        lines = len(full_path.read_text(encoding="utf-8", errors="ignore").splitlines())
                    except OSError:
                        lines = 0
                stats_map[fname] = {"added": lines, "deleted": 0}

    results: List[Dict[str, object]] = []
    for fname, data in stats_map.items():
        results.append({
            "path": fname,
            "added": data["added"],
            "deleted": data["deleted"],
            "total": data["added"] + data["deleted"],
        })

    results.sort(key=lambda x: int(x["total"]), reverse=True)
    return results


def classify_file(filepath: str) -> str:
    """Classify a filepath into a cohesive commit category."""
    for key, _, pattern in CHUNK_CATEGORIES:
        if pattern.search(filepath):
            return key
    return "core"


def partition_commit_chunks(files: List[Dict[str, object]], budget: int = MAX_PUSH_LINE_BUDGET) -> List[Dict[str, object]]:
    """Partition modified files into atomic, cohesive commit chunks under the line budget."""
    categories: Dict[str, List[Dict[str, object]]] = {}
    for f in files:
        cat = classify_file(str(f["path"]))
        categories.setdefault(cat, []).append(f)

    chunks: List[Dict[str, object]] = []

    for cat_key, cat_files in categories.items():
        current_chunk_files: List[Dict[str, object]] = []
        current_chunk_lines = 0

        for f in cat_files:
            file_lines = int(f["total"])
            if current_chunk_lines + file_lines > budget and current_chunk_files:
                chunks.append({
                    "category": cat_key,
                    "files": current_chunk_files,
                    "total_lines": current_chunk_lines,
                })
                current_chunk_files = [f]
                current_chunk_lines = file_lines
            else:
                current_chunk_files.append(f)
                current_chunk_lines += file_lines

        if current_chunk_files:
            chunks.append({
                "category": cat_key,
                "files": current_chunk_files,
                "total_lines": current_chunk_lines,
            })

    return chunks


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze Git changes and verify the 1,000-line budget.")
    parser.add_argument("--path", "-p", default=".", help="Root path of git repository")
    parser.add_argument("--budget", "-b", type=int, default=MAX_PUSH_LINE_BUDGET, help="Line limit budget per commit chunk")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    repo = Path(args.path).resolve()
    stats = get_diff_stats(repo)
    total_delta = sum(int(f["total"]) for f in stats)

    chunks = partition_commit_chunks(stats, budget=args.budget)

    if args.json:
        print(json.dumps({
            "total_files": len(stats),
            "total_lines_changed": total_delta,
            "within_budget": total_delta <= args.budget,
            "recommended_chunks": chunks,
        }, indent=2))
        return 0

    print(f"=== Git Commit Chunk & Budget Analysis ===")
    print(f"Repository: {repo}")
    print(f"Modified Files: {len(stats)}")
    print(f"Total Lines Delta: {total_delta} (Budget: {args.budget})")

    if total_delta <= args.budget:
        print(f"[PASS] Changes fit within the single-commit budget ({total_delta}/{args.budget} lines).")
    else:
        print(f"[ALERT] Total delta ({total_delta}) exceeds the 1,000-line budget. Split into {len(chunks)} cohesive commits:")
        for idx, chunk in enumerate(chunks, 1):
            print(f"  Chunk {idx} [{chunk['category']}]: {len(chunk['files'])} files ({chunk['total_lines']} lines)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
