# Skill Synthesis Protocol (SSP) — Anti-Boilerplate Standard

> **Objective**: Mint crisp, repository-specific `.agents/skills/<project>/SKILL.md` skills containing high-signal domain invariants — strictly banning copy-pasted template repetition.

---

## 1. Anti-Boilerplate Discipline (Lesson from `domodomo` Audit)

Never generate 500-line skills by repeating the same generic 20-bullet checklist across 15 headings. Every minted project skill MUST:
1. State **concrete repo paths** (`src/data/civic/`, `backend/routers/`), never generic abstractions.
2. Document **non-obvious invariants** (e.g., *"English routes stay unprefixed; `/en` redirects 308"*, *"Never import `data/generated/` directly in routes"*).
3. Include the **exact verification commands** from `package.json` / `Makefile` / `CI`.
4. Stay concise (`100–250` lines total, well under the 350-line cap) and pass `python3 scripts/skill_linter.py` with zero boilerplate repetition warnings.

---

## 2. Canonical Project Skill Structure

1. **YAML Frontmatter**: `name` (kebab-case) + specific `description` naming trigger files/domains.
2. **Project Invariants & Data Boundaries**: 3–5 non-negotiables specific to this repo.
3. **Architectural Directory Map**: Exact tree of boundaries and owned modules.
4. **Verification Checklist**: Copy-pasteable commands run before every commit or PR.
5. **Documentation Impact Protocol**: Which docs (`docs/...`, `README.md`) must stay synced when contracts change.
