# How & Why Archaeology Field Manual

> **Objective**: Understand runtime flow, data ownership, and historical design intent before writing a single line of code. Eliminates blind rewrites and subtle regression cascades.

---

## 1. Pass 1 — `/how` (Runtime Execution & Ownership Trace)

Never infer behavior from directory names or file titles alone. Trace the real code path end-to-end:

1. **Locate Entrypoint**: Find the HTTP route handler, CLI `main()`, React Server Component, or event listener.
2. **Trace Ingress Validation**: Check what schema (Zod, Pydantic, JSON Schema) parses raw inputs and what defaults/coercions occur.
3. **Follow State & Side Effects**:
   - Which functions mutate DB rows, files, `IndexedDB`, or caches?
   - Are mutations wrapped in an ACID transaction or idempotency guard?
   - What cleanup hooks exist (`AbortController`, `URL.revokeObjectURL`, `worker.terminate()`, DB `pool.end()`)?
4. **Map Hidden Coupling**:
   - Module-level singletons or in-memory memoization maps.
   - `process.env` reads buried deep inside helper modules instead of top-level config.
   - CSS `transform` / `filter` ancestors breaking `position: fixed` overlays.
   - Implicit ordering dependencies across React `useEffect` or startup hooks.
5. **Determine Blast Radius**: Search all callers (`rg -n "<symbol>"`) and list existing test suites covering this path.

---

## 2. Pass 2 — `/why` (Git & ADR Provenance Mining)

Before deleting an "ugly" check or rewriting an odd condition, check why it exists:

```bash
# Find when and why a specific non-obvious symbol or flag was introduced
git log -S "legacyCompatFlag" -p -n 5

# Inspect commit history with bodies for a target module
git log --follow --format="%h %ad %s%n%b---" -n 10 -- src/services/sync.ts

# Check line-level authorship on a suspicious guard
git blame -L 40,95 src/services/sync.ts
```

### Decision Matrix: Load-Bearing Invariant vs. Accidental Debt

| Observation | Likely Load-Bearing Invariant (Preserve) | Likely Accidental Debt (Subtract) |
| :--- | :--- | :--- |
| **Test Suite** | Dedicated regression test naming edge case or CVE | Zero tests and zero active callers |
| **Commit Message** | Explains browser/OS/upstream API quirk or race condition | Lazy `"wip"` / `"fix"` commit with unused config flag |
| **Data Boundary** | Enforces tenant isolation (`tenant_id`), public/private split, or idempotency | Duplicate formatting helper copy-pasted across files |

---

## 3. Subsystem Brief Output Contract

Before editing an unfamiliar subsystem, produce a concise brief:
- **Flow**: `Entrypoint -> Validator -> Service -> Store` (exact file paths + line numbers).
- **Invariants**: Load-bearing constraints that must remain intact.
- **Shared State / Races**: Concurrent writers, locks, or resource teardown obligations.
- **Test Gate**: Exact test command(s) covering the subsystem today.
