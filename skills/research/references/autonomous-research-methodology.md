# Autonomous Deep Research Methodology (P.A.T.H.S.)

> **Objective**: Unblock broken dependencies, native build failures, and ambiguous architecture decisions rapidly through structured evidence gathering and minimal POCs.

---

## 1. The 4-Phase Pivot Loop

1. **Failure Isolation**: Separate *environment issues* (Node/Python version, missing Xcode CLT, stale lockfile) from *library defects* (unmaintained package, missing ARM64 prebuilds, broken ESM/CJS exports). Capture the exact compiler/runtime error before searching.
2. **Candidate Discovery**: Identify 2–3 serious production candidates via official docs, npm/PyPI release cadence, and issue trackers — avoid obscure 12-star wrappers.
3. **P.A.T.H.S. Scoring Matrix** (`1–5` per axis):
   - **P — Performance**: Throughput, memory overhead, cold-start latency.
   - **A — Activity**: Commits in last 90 days, responsive security triage, clean semver.
   - **T — Type Safety**: First-class TypeScript / Python typing without lagged `@types/*`.
   - **H — Hygiene**: Permissive license (`MIT` / `Apache-2.0` / `BSD`), zero unpatched critical CVEs.
   - **S — Size & Dependencies**: Minimal transitive graph (`< 30 KB` gzipped frontend), zero brittle C++ `node-gyp` build steps.
4. **Minimal Prototype (`playbooks/prototype.md`)**: Write a `20–40` line runnable script in `scratch/` testing real inputs, edge errors, and bundle/runtime compatibility before integrating.

---

## 2. Anti-Guessing Rules
- Never invent package names, CLI flags, or API methods from memory — inspect `package.json`, `node_modules/*/index.d.ts`, or official docs first.
- Record verified library pivots into `.agents/learned_conventions.md` via `/continuous-learning` so future sessions never re-introduce the broken dependency.
