#!/usr/bin/env python3
"""
log_decision_trail.py - DarkNecroStack Decision Trail Ledger (show-me-your-work).

Records structured, auditable decision rows into .agents/memory/decision_trail.tsv
for long, multi-phase, or autonomous engineering runs.
"""

import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path
import sys
from typing import List

HEADER = ["timestamp_utc", "step", "hypothesis", "action", "result", "evidence"]


def sanitize_cell(value: str) -> str:
    """Strip tabs and newlines so TSV structure stays intact."""
    return " ".join(value.replace("\t", " ").splitlines()).strip()


def append_trail_entry(
    trail_path: Path,
    step: str,
    hypothesis: str,
    action: str,
    result: str,
    evidence: str,
) -> Path:
    """Append a single auditable decision row to decision_trail.tsv."""
    trail_path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not trail_path.exists() or trail_path.stat().st_size == 0
    row = [
        datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        sanitize_cell(step),
        sanitize_cell(hypothesis),
        sanitize_cell(action),
        sanitize_cell(result),
        sanitize_cell(evidence),
    ]
    with trail_path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t")
        if write_header:
            writer.writerow(HEADER)
        writer.writerow(row)
    return trail_path


def read_trail(trail_path: Path, tail: int = 20) -> List[List[str]]:
    """Read the last N rows from decision_trail.tsv."""
    if not trail_path.exists():
        return []
    with trail_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle, delimiter="\t"))
    return rows[-tail:] if tail > 0 else rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Append or inspect DarkNecroStack TSV decision trail.")
    parser.add_argument("--trail", default=".agents/memory/decision_trail.tsv", help="Path to TSV file")
    parser.add_argument("--step", help="Workflow step or iteration label")
    parser.add_argument("--hypothesis", default="-", help="Hypothesis tested")
    parser.add_argument("--action", help="Action or command executed")
    parser.add_argument("--result", choices=["PASS", "FAIL", "PIVOT", "INFO"], default="INFO", help="Outcome")
    parser.add_argument("--evidence", default="-", help="Measured proof or file reference")
    parser.add_argument("--show", action="store_true", help="Display recent trail rows")
    args = parser.parse_args()

    trail_path = Path(args.trail)
    if args.show:
        for row in read_trail(trail_path):
            print("\t".join(row))
        return 0

    if not args.step or not args.action:
        print("Error: --step and --action are required unless --show is passed.", file=sys.stderr)
        return 1

    append_trail_entry(trail_path, args.step, args.hypothesis, args.action, args.result, args.evidence)
    print(f"[LOGGED] {args.step} -> {args.result} ({trail_path})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
