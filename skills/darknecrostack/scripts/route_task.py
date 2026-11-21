#!/usr/bin/env python3
"""
route_task.py - DarkNecroStack Dynamic Intent Router & PDS Token Pruner.

Classifies a prompt and repository context into a target playbook, minimal
skill bundle, pruned skills (Platform Domain Specialization), and subagent
worker kickoff instruction.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Set

PLAYBOOK_RULES = [
    ("bug-fix", ("fix", "bug", "error", "broken", "crash", "failing", "regression", "500")),
    ("runtime-forensics", ("oom", "memory leak", "zombie", "unhandled rejection", "objecturl")),
    ("trace-forensics", ("latency", "slow trace", "timeout cascade", "p95", "n+1")),
    ("perf-issue", ("slow", "optimize", "fps", "bundle size", "lighthouse", "lcp", "cls")),
    ("hillclimb", ("benchmark", "eval score", "hillclimb", "throughput", "improve metric")),
    ("refactoring", ("refactor", "decompose", "split file", "strangler", "tech debt", "clean up")),
    ("investigation", ("how does", "why does", "explain", "trace", "understand", "audit")),
    ("visual-parity", ("ui", "design", "mascot", "rive", ".riv", "logo", "icon", "illustration", "css")),
    ("prototype", ("prototype", "which is better", "spike", "compare options", "test if")),
    ("opening-a-pr", ("open pr", "pull request", "push branch", "ship", "babysit")),
    ("figure-it-out", ("migrate", "rewrite", "autonomous", "overnight", "full-scale", "ecosystem")),
]


def detect_platform_targets(repo_path: Path, prompt_lower: str) -> Set[str]:
    """Detect client platform targets from repo manifests and prompt signals."""
    platforms: Set[str] = set()
    if (repo_path / "pubspec.yaml").exists() or any(k in prompt_lower for k in ("flutter", "swiftui", "compose", "ios", "android", "mobile", "react native")):
        platforms.add("mobile")
    if (repo_path / "package.json").exists() or any(k in prompt_lower for k in ("next.js", "react", "tailwind", "web", "css", "html", "vite")):
        platforms.add("web")
    if any(k in prompt_lower for k in ("mcp", "model context protocol")):
        platforms.add("mcp")
    if any(k in prompt_lower for k in ("mascot", ".riv", "rive", "lottie", "2d character")):
        platforms.add("mascot")
    if any(k in prompt_lower for k in ("logo", "favicon", "squircle", "brand asset", "illustration", "og card")):
        platforms.add("brand")
    if any(k in prompt_lower for k in ("canvas", "webaudio", "wasm", "webassembly", "pdf", "objecturl")):
        platforms.add("media")
    if any(k in prompt_lower for k in ("indexeddb", "opfs", "offline-first", "local-first", "public-data")):
        platforms.add("local_data")
    return platforms


def match_playbook(prompt_lower: str) -> str:
    """Match prompt text to the highest-priority DarkNecroStack playbook."""
    for playbook, keywords in PLAYBOOK_RULES:
        if any(kw in prompt_lower for kw in keywords):
            return playbook
    return "feature"


def build_skill_bundle(playbook: str, platforms: Set[str], repo_path: Path) -> Dict[str, List[str]]:
    """Select active and PDS-pruned skills for minimal token overhead."""
    active: List[str] = ["darknecrostack", "prove-it-works"]
    pruned: List[str] = []

    if playbook in {"investigation", "bug-fix", "runtime-forensics", "trace-forensics"}:
        active.append("code-archaeology")
    if playbook in {"feature", "refactoring", "figure-it-out"}:
        active.extend(["architect", "interrogate"])
    if playbook in {"hillclimb", "prototype"}:
        active.append("arena")
    if playbook == "visual-parity" or platforms.intersection({"web", "mobile", "mascot", "brand"}):
        active.extend(["ui", "anti-slop"])
    if "web" in platforms and "mobile" not in platforms:
        active.append("web-ui")
        pruned.append("mobile-ui")
    elif "mobile" in platforms and "web" not in platforms:
        active.append("mobile-ui")
        pruned.append("web-ui")
    elif "web" in platforms and "mobile" in platforms:
        active.extend(["web-ui", "mobile-ui"])
    else:
        pruned.extend(["web-ui", "mobile-ui"])

    platform_map = {
        "mascot": "2d-mascot-motion",
        "brand": "brand-assets",
        "mcp": "mcp-engineering",
        "media": "browser-media-wasm",
        "local_data": "local-first-data",
    }
    for key, skill_name in platform_map.items():
        if key in platforms:
            active.append(skill_name)

    if playbook == "figure-it-out":
        active.append("full-scale-mode")

    worker_path = (repo_path / "skills" / "darknecrostack" / "worker.md").resolve()
    return {
        "active_skills": list(dict.fromkeys(active)),
        "pruned_skills": list(dict.fromkeys(pruned)),
        "estimated_tokens_saved": [str(len(pruned) * 1850)],
        "worker_kickoff": [f"Read {worker_path} before anything else."],
    }


def route_prompt(prompt: str, repo_path: Path) -> Dict[str, object]:
    """Compute full routing decision for a given prompt and repo."""
    prompt_lower = prompt.lower()
    playbook = match_playbook(prompt_lower)
    platforms = detect_platform_targets(repo_path, prompt_lower)
    bundle = build_skill_bundle(playbook, platforms, repo_path)
    return {
        "playbook": f"skills/darknecrostack/playbooks/{playbook}.md",
        "detected_platforms": sorted(platforms),
        "active_skills": bundle["active_skills"],
        "pruned_skills": bundle["pruned_skills"],
        "estimated_tokens_saved": int(bundle["estimated_tokens_saved"][0]),
        "subagent_kickoff_line_1": bundle["worker_kickoff"][0],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Route a prompt via DarkNecroStack dynamic engine.")
    parser.add_argument("--prompt", "-p", required=True, help="Incoming user prompt")
    parser.add_argument("--path", default=".", help="Workspace repository path")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    args = parser.parse_args()

    decision = route_prompt(args.prompt, Path(args.path).resolve())
    if args.json:
        print(json.dumps(decision, indent=2))
        return 0

    print("=== DarkNecroStack Dynamic Route ===")
    print(f"Playbook         : {decision['playbook']}")
    print(f"Platforms        : {', '.join(decision['detected_platforms']) or 'none'}")
    print(f"Active Skills    : {', '.join(decision['active_skills'])}")
    print(f"Pruned (PDS)     : {', '.join(decision['pruned_skills']) or 'none'} (~{decision['estimated_tokens_saved']} tokens saved)")
    print(f"Subagent Line 1  : {decision['subagent_kickoff_line_1']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
