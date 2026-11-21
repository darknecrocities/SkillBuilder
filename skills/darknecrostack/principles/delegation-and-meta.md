# Delegation & Meta Principles

Read these principles when managing context budgets, spawning subagents, deciding whether to ask the user, or noticing repeated friction.

---

## 1. Guard the Context Window
- **When it applies**: Long sessions, large log outputs, broad repository searches, or multi-track builds.
- **Rule**: Keep the main coordinator thread lean. Delegate bulky file sweeps, independent research, and partitioned implementation tracks to subagents (`worker.md` first!), passing file pointers rather than pasting massive file contents inline. Keep only crisp summaries, interface contracts, and verification receipts in the main context.

## 2. Never Block on the Human
- **When it applies**: Tempted to ask `"Should I run X?"`, `"Which library works here?"`, or `"Can I check this?"` on reversible local work.
- **Rule**: For reversible decisions, proceed, run the prototype or diagnostic check (`playbooks/prototype.md`), verify the outcome, and present the concrete result. Reserve human interruptions for genuinely irreversible actions (destructive DB/file deletion, force-push, production deploy) or ambiguous business requirements that alter data/auth architecture.

## 3. Encode Lessons in Structure
- **When it applies**: Catching yourself repeating the same rule, correcting the same AI slop pattern, or writing the same instruction twice.
- **Rule**: Do not add another paragraph of prose reminding the model not to make the mistake. Encode the invariant structurally as a linter rule (`skill_linter.py`, `sanitize_ai_slop.py`), a hook (`hooks.json`), a schema type, a test assertion, or a generator script (`scripts/`).
