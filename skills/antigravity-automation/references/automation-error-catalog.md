# Antigravity Automation, Sidecars & Hooks Error Catalog

> **Objective**: Rapid diagnosis and resolution of scheduled sidecar, `schedule` tool, and `hooks.json` lifecycle gate failures.

---

## 1. Common Automation & Hook Failure Modes

| Failure Signature | Root Cause | Production Remediation |
| :--- | :--- | :--- |
| **Hook timeout / tool call blocked unexpectedly** | Hook script hangs waiting on stdin, runs slow full-repo `os.walk`, or exceeds `timeout: 5`s. | Read tool payload quickly from stdin/args, scan only the single target file in `PostToolUse`, keep execution `< 300ms`. |
| **Scheduled sidecar fires at wrong local hour** | Missing `CRON_TZ` in `~/.gemini/jetski/sidecars/<slug>/sidecar.json` (defaults to UTC). | Explicitly set `"cron_tz": "Asia/Manila"` (or user's IANA timezone) in sidecar manifest. |
| **Agent stuck in `sleep()` polling loop** | Using `run_command("sleep 10")` or looping `manage_task(status)` instead of reactive wakeup. | Stop calling tools or use native `schedule(DurationSeconds, TimerCondition)` — system wakes automatically on message arrival. |
| **Subagent ignores `hooks` or project rules** | Spawned worker lacked explicit `worker.md` pointer and file ownership list. | Start subagent kickoff with `Read <abs>/skills/darknecrostack/worker.md before anything else.` |
| **PostToolUse hook rejects legitimate large doc** | Applying 500-line *source* rule blindly to generated lockfiles, `.sql` dumps, or assets. | Restrict line-guard checks to code extensions (`.py`, `.ts`, `.tsx`, `.js`, `.jsx`, `.go`, `.rs`, `.dart`, `.swift`, `.kt`). |

---

## 2. Hook Safety Checklist
- Always verify hook scripts locally with `python3 skills/antigravity-automation/scripts/verify_antigravity_hooks.py` before committing `hooks.json`.
- Ensure `PreToolUse` safety gates catch destructive `rm -rf`, `DROP TABLE`, `TRUNCATE`, and `git push --force` cleanly with clear recovery guidance.
