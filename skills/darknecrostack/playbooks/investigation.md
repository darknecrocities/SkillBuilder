# Playbook: Investigation

Use when exploring how an unfamiliar subsystem works, why it exists, or mapping blast radius before proposing changes.

## Steps
1. **Restate Scope**: Name the question to answer and the target entrypoints.
2. **Trace Flow (`/code-archaeology` How)**: Follow entrypoint -> validation -> domain service -> persistence -> side effects -> callers. Record file paths and exact symbol names.
3. **Trace Intent (`/code-archaeology` Why)**: Run `git log -S` / `git blame` on non-obvious branches or guards to identify intentional invariants ("load-bearing quirks") vs accidental debt.
4. **Map Contracts & Boundaries**: List external schemas, shared mutable state, env vars, and active tests covering this subsystem.
5. **Emit Subsystem Brief**: Present observed facts (`[measured]` from files read), inferred behavior (`[inferred]`), and open risks. Stop before editing unless requested.
