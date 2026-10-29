# Antigravity Automation Error Catalog & Failure Remediation

Master catalog of common automation errors across scheduled sidecars, in-session scheduling, background daemons, and lifecycle hooks.

---

## Error Catalog Table

Error Signature | Root Cause | Impact | Automated Remediation
:--- | :--- | :--- | :---
`ERR-AUTO-001: Cron Field Count Mismatch` | Cron expression does not have exactly 5 fields | Sidecar fails to register or silently never triggers | Run `generate_sidecar_automation.py` to validate expression. Ensure standard 5-field syntax (`* * * * *`).
`ERR-AUTO-002: Missing CRON_TZ Prefix` | Sidecar schedule lacks IANA timezone identifier | Triggers in UTC rather than user's local timezone | Always prepend `CRON_TZ=<IANA_TZ>` (e.g. `CRON_TZ=America/New_York`).
`ERR-AUTO-003: Shell Sleep Polling Anti-Pattern` | Agent invoked `sleep` in `run_command` in a loop | Wastes turn budget, blocks reactive messages | Replace busy-wait loops with the `schedule` tool or background async tasks (`WaitMsBeforeAsync: 500`).
`ERR-AUTO-004: Orphan Daemon Task` | Background task launched without supervisor monitoring | Consumes CPU/memory indefinitely | Query `manage_task(Action="list")` and terminate hung processes via `manage_task(Action="kill", TaskId=...)`.
`ERR-AUTO-005: Hook Timeout Overrun` | Hook script exceeded declared `timeout` in seconds | Antigravity kills the hook and logs warning | Optimize hook script to complete within <2s. Defer expensive computations to background tasks.
`ERR-AUTO-006: Missing Hook Script Target` | `hooks.json` references non-existent script path | Hook fails to run on lifecycle trigger | Run `verify_antigravity_hooks.py` to audit file paths against the repository root.
