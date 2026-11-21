# Multi-Agent Orchestration & Parallel Execution Manual

> **Objective**: Coordinate parallel subagents safely without overlapping edits, lost context, rule amnesia, or redundant storage backups.

---

## 1. Mandatory Subagent Kickoff Protocol

Every subagent launched via `invoke_subagent` or `swarm` starts with an isolated context and **does not inherit slash-command skills**. Structure every brief identically:
1. **Line 1**: `Read <abs-path>/skills/darknecrostack/worker.md before anything else.`
2. **Goal**: One sentence stating the user-facing outcome.
3. **Owned Files**: Exact paths this worker may create/modify (zero overlap with sibling workers).
4. **Forbidden Files / Guardrails**: Paths owned by other tracks + active `.agents/learned_conventions.md` rules.
5. **Proof Command**: Exact test/linter command the worker must run and report `[measured]` before returning.

---

## 2. Parallelism & Isolation Matrix

| Scenario | Recommended Workspace Mode | Coordination Rule |
| :--- | :--- | :--- |
| **Read-only audit / research / QA** | `inherit` | Zero writes; aggregate findings in parent thread. |
| **Disjoint domain tracks (Frontend vs Backend)** | `inherit` (strict file partition) | Partition directories explicitly (`src/ui/` vs `src/api/`). |
| **Competing prototypes (`/arena`) or risky refactors** | `share` or `branch` | Isolated working copy; parent reviews diff and grafts winner cleanly. |

---

## 3. Reactive Wakeup & Storage Sync
- **Zero Polling**: End turn or continue independent work after spawning subagents; the messaging runtime wakes the coordinator automatically when results arrive.
- **Single-Slot Backups**: Coordinate database/cloud mutations through `.backups/backup_manifest.json` (`manage_deduplicated_backup.py`) to prevent duplicate `.bak.1` spam across concurrent workers.
- **Fresh Subagents on Retry**: Dispatch follow-up fixes to a fresh subagent carrying the original brief + prior report unless expensive local state makes resuming mandatory.
