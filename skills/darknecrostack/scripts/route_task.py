#!/usr/bin/env python3
"""
route_task.py - DarkNecroStack Dynamic Intent Router, Combo Resolver & PDS Pruner.

Classifies a prompt or named combo preset into a target playbook, minimal
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

COMBO_PRESETS: Dict[str, Dict[str, object]] = {
    "combo-fullstack-web": {
        "category": "Fullstack & Web Product",
        "skills": ["architect", "fullstack", "backend", "api-design", "database", "frontend", "web-ui", "routing", "state-management", "testing", "security"],
        "pruned": ["mobile-ui", "3d"],
    },
    "combo-landing-brand": {
        "category": "Fullstack & Web Product",
        "skills": ["anti-slop", "ui", "web-ui", "brand-assets", "2d-mascot-motion", "3d", "performance"],
        "pruned": ["mobile-ui", "database"],
    },
    "combo-cv-vlm-edge": {
        "category": "AI, Computer Vision, VLM & Local LLM",
        "skills": ["computer-vision", "vlm-multimodal", "local-llm", "ai-integration", "performance", "testing"],
        "pruned": ["web-ui", "mobile-ui"],
    },
    "combo-hybrid-ai-app": {
        "category": "AI, Computer Vision, VLM & Local LLM",
        "skills": ["ai", "local-llm", "ai-integration", "backend", "frontend", "web-ui", "security", "testing"],
        "pruned": ["mobile-ui"],
    },
    "combo-mobile-offline": {
        "category": "Mobile & Offline-First",
        "skills": ["mobile-ui", "frontend", "routing", "state-management", "local-first-data", "qa", "testing"],
        "pruned": ["web-ui"],
    },
    "combo-cloud-data": {
        "category": "Cloud, Serverless & Data",
        "skills": ["gcp", "aws", "firebase", "supabase", "devops", "database", "data-pipelines", "observability", "security"],
        "pruned": ["web-ui", "mobile-ui"],
    },
    "combo-mcp-media": {
        "category": "MCP, Browser Media & Desktop",
        "skills": ["mcp-engineering", "browser-media-wasm", "local-first-data", "security", "testing"],
        "pruned": ["mobile-ui"],
    },
    "combo-ab-ship": {
        "category": "Audit, A/B Testing, Refactor & Release",
        "skills": ["code-archaeology", "testing", "qa", "interrogate", "prove-it-works", "git-workflow"],
        "pruned": ["3d"],
    },
    "combo-safe-refactor": {
        "category": "Audit, A/B Testing, Refactor & Release",
        "skills": ["code-archaeology", "refactor", "testing", "interrogate", "prove-it-works"],
        "pruned": ["3d"],
    },
}


def detect_platform_targets(repo_path: Path, prompt_lower: str) -> Set[str]:
    """Detect client, app, AI, CV, VLM, and tooling targets from repo manifests and prompt signals."""
    platforms: Set[str] = set()
    if (repo_path / "pubspec.yaml").exists() or any(k in prompt_lower for k in ("flutter", "swiftui", "compose", "ios", "android", "mobile", "react native", "ipad", "foldable")):
        platforms.add("mobile")
    if (repo_path / "package.json").exists() or any(k in prompt_lower for k in ("next.js", "react", "tailwind", "web", "css", "html", "vite")):
        platforms.add("web")
    if any((repo_path / f).exists() for f in ("src-tauri", "electron.vite.config.ts", "electron-builder.yml")) or any(k in prompt_lower for k in ("electron", "tauri", "desktop app", "offline app")):
        platforms.add("app")
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
    if any(k in prompt_lower for k in ("opencv", "cv2", "yolo", "onnx", "mediapipe", "sam2", "bytetrack", "ocr", "computer vision")):
        platforms.add("cv")
    if any(k in prompt_lower for k in ("vlm", "multimodal", "qwen2.5-vl", "qwen-vl", "gemma 3", "florence-2", "mmproj", "mlx-vlm", "grounding")):
        platforms.add("vlm")
    if (repo_path / "Modelfile").exists() or any(k in prompt_lower for k in ("ollama", "llama.cpp", "llama-server", "gguf", "mlx", "vllm", "sglang", "webllm", "local llm")):
        platforms.add("local_llm")
    if any(k in prompt_lower for k in ("model gateway", "ai integration", "hybrid fallback", "cv+vlm")):
        platforms.add("ai_integration")
    if any(k in prompt_lower for k in ("a/b test", "ab test", "srm")):
        platforms.add("ab_test")
    return platforms


def match_playbook(prompt_lower: str, platforms: Set[str] | None = None) -> str:
    """Match prompt text and detected platforms to the highest-priority DarkNecroStack playbook."""
    active_platforms = platforms or set()
    mobile_layout_kw = ("responsive", "adaptive", "tablet", "foldable", "split view", "split screen", "safe area", "size class", "windowsizeclass", "landscape")
    if "mobile" in active_platforms and any(k in prompt_lower for k in mobile_layout_kw):
        return "mobile-responsive"
    if ("web" in active_platforms and "mobile" in active_platforms) or any(k in prompt_lower for k in ("dynamic routing", "cross-platform", "mobile and web", "app and web")):
        return "dynamic-platform-routing"
    for playbook, keywords in PLAYBOOK_RULES:
        if any(kw in prompt_lower for kw in keywords):
            return playbook
    return "feature"


def _apply_client_pds(platforms: Set[str], active: List[str], pruned: List[str]) -> None:
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

    _apply_client_pds(platforms, active, pruned)

    platform_map = {
        "mascot": "2d-mascot-motion",
        "brand": "brand-assets",
        "mcp": "mcp-engineering",
        "media": "browser-media-wasm",
        "local_data": "local-first-data",
        "cv": "computer-vision",
        "vlm": "vlm-multimodal",
        "local_llm": "local-llm",
        "ai_integration": "ai-integration",
        "ab_test": "testing",
    }
    for key, skill_name in platform_map.items():
        if key in platforms:
            active.append(skill_name)
        elif key in {"cv", "vlm", "local_llm"}:
            pruned.append(skill_name)

    if {"cv", "vlm", "local_llm"}.intersection(platforms) and "ai-integration" not in active:
        active.append("ai-integration")
    if "app" in platforms:
        for s in ("frontend", "local-first-data", "browser-media-wasm"):
            if s not in active:
                active.append(s)
    if playbook == "figure-it-out":
        active.append("full-scale-mode")

    worker_path = (repo_path / "skills" / "darknecrostack" / "worker.md").resolve()
    return {
        "active_skills": list(dict.fromkeys(active)),
        "pruned_skills": list(dict.fromkeys(pruned)),
        "estimated_tokens_saved": [str(len(set(pruned)) * 1850)],
        "worker_kickoff": [f"Read {worker_path} before anything else."],
    }


def route_combo(combo_name: str, repo_path: Path) -> Dict[str, object]:
    """Resolve a categorized multi-skill combo preset cleanly."""
    if combo_name not in COMBO_PRESETS:
        raise ValueError(f"Unknown combo '{combo_name}'. Available: {sorted(COMBO_PRESETS)}")
    preset = COMBO_PRESETS[combo_name]
    worker_path = (repo_path / "skills" / "darknecrostack" / "worker.md").resolve()
    active = ["darknecrostack", *preset["skills"], "prove-it-works"]  # type: ignore[misc]
    pruned: List[str] = list(preset["pruned"])  # type: ignore[arg-type]
    return {
        "playbook": "skills/darknecrostack/playbooks/combo-stacks.md",
        "combo": combo_name,
        "category": preset["category"],
        "detected_platforms": [],
        "active_skills": list(dict.fromkeys(active)),
        "pruned_skills": pruned,
        "estimated_tokens_saved": len(pruned) * 1850,
        "subagent_kickoff_line_1": f"Read {worker_path} before anything else.",
    }


def route_prompt(prompt: str, repo_path: Path) -> Dict[str, object]:
    """Compute full routing decision for a given prompt and repo."""
    prompt_lower = prompt.lower()
    platforms = detect_platform_targets(repo_path, prompt_lower)
    playbook = match_playbook(prompt_lower, platforms)
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
    parser = argparse.ArgumentParser(description="Route a prompt or combo preset via DarkNecroStack.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--prompt", "-p", help="Incoming user prompt")
    group.add_argument("--combo", "-c", choices=sorted(COMBO_PRESETS), help="Categorized multi-skill combo preset")
    parser.add_argument("--path", default=".", help="Workspace repository path")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    args = parser.parse_args()

    repo = Path(args.path).resolve()
    decision = route_combo(args.combo, repo) if args.combo else route_prompt(args.prompt, repo)
    if args.json:
        print(json.dumps(decision, indent=2))
        return 0

    print("=== DarkNecroStack Dynamic Route ===")
    print(f"Playbook         : {decision['playbook']}")
    if decision.get("combo"):
        print(f"Combo ({decision['category']}): {decision['combo']}")
    else:
        print(f"Platforms        : {', '.join(decision['detected_platforms']) or 'none'}")
    print(f"Active Skills    : {', '.join(decision['active_skills'])}")
    print(f"Pruned (PDS)     : {', '.join(decision['pruned_skills']) or 'none'} (~{decision['estimated_tokens_saved']} tokens saved)")
    print(f"Subagent Line 1  : {decision['subagent_kickoff_line_1']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
