# Convention Persistence & Deduplication Manual

> **Objective**: Ensure user corrections, repository invariants, and hard-won debugging discoveries persist cleanly across sessions without polluting `.agents/learned_conventions.md` with duplicate or stale notes.

---

## 1. What Deserves Persistence vs. What Does Not

| Persist in `.agents/learned_conventions.md` | Do NOT Persist |
| :--- | :--- |
| Explicit architectural invariants (*"All civic data reads go through `src/data/civic/`"*) | One-off task status (*"Fixed typo in header.tsx"*) |
| Verified build/test commands & required flags | Speculative guesses or unverified workarounds |
| Library/OS pitfalls discovered during debugging | Duplicate restatements of global `AGENTS.md` rules |
| Explicit user formatting/UI/naming preferences | Secrets, API keys, or environment credentials |

---

## 2. Canonical Entry Format & Deduplication

Use `scripts/record_learning.py` so entries are normalized, timestamped, tagged by domain, and deduplicated before appending:

```bash
python3 skills/continuous-learning/scripts/record_learning.py \
  --category "Routing" \
  --rule "Default English routes stay unprefixed; /en redirects 308 to canonical path"
```

### Graduating Repeated Rules into Structure (`Encode Lessons in Structure`)
If the same convention has to be enforced 3+ times manually:
1. Encode it as a linter check (`skill_linter.py`, `sanitize_ai_slop.py`), a schema type, or an automated test.
2. Promote project-wide multi-rule invariants into a dedicated project skill via `/project-skills` (`SSP`).
