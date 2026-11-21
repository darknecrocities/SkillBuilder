# Playbook: Pause Safely

Use when halting work mid-flight, waiting on user confirmation for an irreversible gate, or handing off cleanly.

## Steps
1. **Never Leave Broken Syntax**: Ensure no half-written files or failing syntax errors remain in the workspace.
2. **Checkpoint Memory & Trail**: Record current stage, touched files, and pending risks in `orchestration_state.json` and `decision_trail.tsv`.
3. **Emit Clean Handoff**: Summarize exact verified checks `[measured]`, uncommitted/committed branch state, and the single decision or confirmation needed to resume.
