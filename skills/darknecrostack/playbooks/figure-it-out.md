# Playbook: Figure It Out (`figure-it-out`)

Use when a task is large, cross-cutting, unattended, or does not match a single narrow playbook.

## Steps
1. **Decompose into Verifiable Units**: Break the goal into sequential milestones where each unit ends in an automated test, linter, or script check.
2. **Initialize Tracking**: Initialize `.agents/memory/orchestration_state.json` via `/full-scale-mode` and open `.agents/memory/decision_trail.tsv` via `log_decision_trail.py`.
3. **Design Before Building**: Run `/code-archaeology` on touched subsystems and `/architect` to lock interfaces and non-overlapping file ownership.
4. **Build the Lever**: Write reusable scripts/generators (`Build the Lever`) when repeating work across 3+ modules or skills.
5. **Execute & Checkpoint**: Dispatch partitioned subagents (kickoff line 1: `Read <abs>/worker.md before anything else.`), logging each step and verification outcome to `decision_trail.tsv`.
6. **Harness & Release**: Run `/interrogate`, `/prove-it-works`, and `orchestration_harness.py` before opening the PR.
