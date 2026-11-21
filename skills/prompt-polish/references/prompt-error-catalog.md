# Prompt Defect & Ambiguity Error Catalog

> **Objective**: Catch underspecified requirements, conflicting constraints, and hallucination triggers *before* generating code.

---

## 1. Common Prompt Defects & Deterministic Fixes

| Defect Pattern | Example Raw Prompt | Polished RFC Remediation |
| :--- | :--- | :--- |
| **Missing Persistence Target** | *"Build a user dashboard with tasks"* | Declare real store explicitly (`SQLite better-sqlite3` or `PostgreSQL`), zero mock arrays. |
| **Unbounded Platform Scope** | *"Make a sleek responsive UI"* | Lock target (`Web React 19 + Tailwind v4` OR `Flutter 120Hz`) and 1 `/ui` art movement. |
| **Undefined Error & Timeout Semantics** | *"Fetch data from third-party API"* | Mandate `3s` connect / `15s` read timeouts, bounded jitter retries on `5xx`, RFC 7807 error envelope. |
| **Unverified Mascot / Logo Ask** | *"Add a cool AI mascot and logo"* | Route to `/2d-mascot-motion` (`.riv` or `<35`-node SVG rig) and `/brand-assets` (4 logo stress tests + squircle), banning emoji/blurry raster slop. |
| **Silent Security Gaps** | *"Add file read tool and user profile endpoint"* | Mandate `realpath` workspace sandboxing (`/mcp-engineering`) and tenant scoping `WHERE id = $1 AND tenant_id = $2` (`/security`). |
| **Missing Proof Gate** | *"Update the tests and ship"* | Append exact verification commands (`npm test`, `skill_linter.py`, `verify_all_skills.sh`) and `[measured]` output contract. |

---

## 2. When to Ask vs. Proceed
- **Ask (Focused Multiple-Choice)**: Only when ambiguity alters fundamental DB choice, auth model, or irreversible destructive behavior.
- **Proceed with Explicit Defaults**: For reversible layout, tooling, or implementation details — run a quick prototype (`playbooks/prototype.md`) and state assumptions clearly.
