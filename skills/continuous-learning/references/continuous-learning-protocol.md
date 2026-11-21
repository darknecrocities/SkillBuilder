# Continuous Conversational Learning Protocol (CLP)

> **Objective**: Absorb user corrections immediately within the active turn and turn recurring friction into permanent structural guardrails.

---

## 1. The 4-Step CLP Execution Loop

1. **Detect Correction / Invariant**: Trigger whenever the user says *"always use X"*, *"don't do Y"*, *"never edit generated JSON directly"*, or corrects an agent assumption.
2. **Apply Immediately**: Update the active plan, code diff, and tests in the same turn — never wait for a future session.
3. **Persist Atomically**: Record a crisp, one-sentence imperative rule into `.agents/learned_conventions.md` via `record_learning.py`.
4. **Verify Before Done**: Re-read `.agents/learned_conventions.md` during Stage 1 (`Discover`) and Stage 4 (`Verify`) so zero corrected mistakes regress.

---

## 2. Handling Conflicting Rules
- **Precedence Order**: Explicit current user directive > Project `.agents/learned_conventions.md` > Project `AGENTS.md` > Global defaults.
- When a new user directive supersedes an old learned rule, **edit or remove** the obsolete line instead of leaving contradictory rules side-by-side.

---

## 3. Subagent Propagation Rule
Because spawned subagents start with blank conversational memory, pass any relevant conventions from `.agents/learned_conventions.md` inside the subagent's brief alongside `Read <abs>/skills/darknecrostack/worker.md before anything else.`
