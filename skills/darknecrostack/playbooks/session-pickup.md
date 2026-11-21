# Playbook: Session Pickup

Use when resuming work across context compaction, a new session, or an interrupted branch.

## Steps
1. **Read State Before Code**: Inspect `git status -sb`, `git log -n 5 --oneline`, `.agents/memory/orchestration_state.json`, `.agents/memory/decision_trail.tsv`, and `.agents/learned_conventions.md`.
2. **Verify Current Baseline**: Re-run the active test/lint check to confirm whether the working tree is green or mid-failure before making new edits.
3. **Reconcile Remaining Milestones**: Identify completed vs pending milestones and state the exact next verifiable unit to execute.
