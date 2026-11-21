# Five-Lens Adversarial Audit Manual

> **Objective**: Inspect every diff with hostile engineering rigor before commit or PR creation, catching silent failures, security holes, lifecycle leaks, and AI slop.

---

## 1. Lens-by-Lens Defect Matrix

| Lens | What AI Code Commonly Breaks | Mandatory Fix |
| :--- | :--- | :--- |
| **1. Correctness** | Empty `catch (e) {}`, unvalidated `JSON.parse()`, partial multi-step writes without transaction, stale async responses overwriting newer queries. | Propagate typed/RFC 7807 errors, validate with Zod/Pydantic at boundaries, wrap multi-writes in transactions, wire `AbortController`. |
| **2. Security & Data** | SQL/shell string interpolation, `WHERE id = $1` missing `tenant_id` (BOLA), `path.join` traversal in MCP tools, outbound `fetch(userUrl)` without DNS/private-IP block (SSRF), private raw data leaked to public exports. | Parameterized queries, `shell=False` arg arrays, `WHERE id = $1 AND tenant_id = $2`, `realpath` prefix checks, post-DNS IP pinning. |
| **3. Concurrency & Leaks** | Unrevoked `URL.createObjectURL()`, orphaned `new Worker()`, undisposed Rive `.riv` or Three.js geometries, unclosed `AudioContext`, missing `clearInterval`. | Pair every allocation with `try/finally` or React/Flutter unmount disposal; add leak regression tests. |
| **4. Performance** | N+1 DB queries inside `for` loops, heavy Canvas/JSON parsing on main UI thread, unclamped `devicePixelRatio` (`>2`), bloated files (`>350` lines). | Batch queries (`WHERE id = ANY($1)`), offload media to Web Workers, clamp DPR `<= 2`, decompose at 350 lines. |
| **5. Diff Unslop** | One-caller pass-through wrappers, unused imports/props, obvious comments (`// set loading true`), `shields.io` badges, mock arrays, purple gradients, `zinc-500` low contrast. | Delete dead abstractions and obvious comments; run `sanitize_ai_slop.py --strict`. |

---

## 2. Surgical Diff Unslop Checklist (`no-comments` & Subtraction)

Inspect `git diff` line-by-line before committing:
- [ ] **Comment Audit**: Every remaining comment explains *why* (invariant, browser quirk, concurrency order), never *what* syntax does.
- [ ] **Abstraction Audit**: No helper function or interface exists for a single trivial caller unless it clarifies a complex boundary.
- [ ] **Scope Audit**: Zero unrequested refactors or formatting churn on untouched files.
- [ ] **Verification Audit**: All tests, linters, and line-limit checks ran *after* the final edit.
