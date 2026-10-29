# Continuous Conversational Learning Protocol (CLP)

The Continuous Learning Protocol (CLP) ensures that user corrections, project preferences, and custom conventions are absorbed immediately and persisted permanently across turns.

---

## 1. The CLP Lifecycle

```text
User Correction / Direct Feedback
       ↓
Parse Negative Constraint ("Never use X", "Always do Y")
       ↓
Run scripts/record_learning.py with structured parameters
       ↓
Verify persistence in .agents/learned_conventions.md
       ↓
Enforce invariant on all subsequent generations
```

---

## 2. Invariant Criteria

Valid Invariant | Invalid Bloat
:--- | :---
Deterministic rule ("Always prefix test files with `test_`") | Transient task status ("Working on step 3")
Architecture preference ("Use Zustand slices rather than Redux") | General coding common sense ("Write clean code")
Explicit user style ("Prohibit emojis in buttons") | Verbose conversation summaries
