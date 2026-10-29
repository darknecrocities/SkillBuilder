# Convention Persistence & Storage Standards

Conventions must be saved to `.agents/learned_conventions.md` to ensure automatic discovery by Antigravity and other agent engines.

---

## 1. Markdown Format Specification

```markdown
# Learned Conventions & Workspace Invariants

## Invariants
- [YYYY-MM-DD] Category: Rule description with exact file patterns.
- [2026-10-29] Testing: All mock APIs must use MSW handlers under `tests/mocks/`.
- [2026-10-29] Styling: Enforce Lucide SVG icons with `aria-hidden="true"`.
```

---

## 2. Programmatic Recording Utility

Always execute `scripts/record_learning.py`:
```bash
python3 skills/continuous-learning/scripts/record_learning.py \
    --category "Architecture" \
    --rule "All backend API errors must conform to RFC 7807 Problem Details."
```
