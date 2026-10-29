# Antigravity Scheduled Sidecars Guide

Google Antigravity supports scheduled background automations implemented via background sidecars (`"builtin": "schedule"`). Each scheduled sidecar executes in a fresh isolated conversation context (`agentapi new-conversation`) according to a standard 5-field cron schedule.

---

## 1. Directory Structure & Path Conventions

Scheduled sidecars are registered under the user's global jetski directory:
```text
~/.gemini/jetski/sidecars/<slug>/sidecar.json
```

Where:
- `<slug>`: Lowercase hyphenated unique identifier (e.g., `daily-repo-health-audit`, `weekly-security-scan`).
- `sidecar.json`: Configuration manifest declaring schedule, timezone, and execution prompt.

---

## 2. Canonical Manifest Schema

```json
{
  "builtin": "schedule",
  "args": {
    "schedule": "CRON_TZ=America/New_York 0 9 * * 1-5",
    "prompt": "Inspect git status, run verify_all_skills.sh, and summarize changes in a morning report."
  }
}
```

### Key Properties:
- **`builtin`**: Must strictly be `"schedule"`.
- **`args.schedule`**: Standard 5-field cron string prefixed with `CRON_TZ=<IANA_TZ>`.
- **`args.prompt`**: Self-contained markdown prompt instructing the agent on what to inspect, execute, and report.

---

## 3. Five-Turn Interactive Authoring Protocol

When designing a scheduled automation interactively with a user:

1. **Turn 1 — Cadence Selection**:
   Prompt via `ask_question`: `Hourly`, `Daily`, `Weekly`, or `Custom cron schedule`.
2. **Turn 2 — Specific Hour & Days**:
   Confirm exact execution time (e.g. `9:00 AM`) and active weekdays.
3. **Turn 3 — Self-Contained Task Prompt**:
   Solicit open-ended goal and refine it into an actionable instruction with explicit verification checks.
4. **Turn 4 — Write Manifest**:
   Generate `~/.gemini/jetski/sidecars/<slug>/sidecar.json` using `generate_sidecar_automation.py`.
5. **Turn 5 — Verification & Test Run**:
   Validate via `agentapi new-conversation` or inspect active schedules via `--list`.
