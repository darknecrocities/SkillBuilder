# Verification & Evidence Contract Manual

> **Objective**: Enforce empirical proof over assumptions. Every reported result must trace to an executable check run after the final edit.

---

## 1. Proof Strength Hierarchy (Weakest -> Strongest)

| Tier | Verification Method | Sufficient Alone? | What It Proves |
| :--- | :--- | :---: | :--- |
| **Level 1** | Syntax / Typecheck (`tsc --noEmit`, `py_compile`) | **No** | Types and grammar parse cleanly; says nothing about runtime logic. |
| **Level 2** | Behavior Unit Tests (`unittest`, `vitest`) | Conditional | Core pure logic, edge cases, and boundary schemas hold under deterministic inputs. |
| **Level 3** | Integration / Contract Tests (SQLite/Postgres/HTTP/MCP) | Yes (Backend) | Real queries, migrations, RFC 7807 error envelopes, and path sandboxes work end-to-end. |
| **Level 4** | Asset, Visual & E2E Auditors (`verify_mascot_assets.py`, Playwright) | Yes (UI/Assets) | Viewport responsiveness (`375px–1920px+`), WCAG contrast, `<35`-node SVGs, and user flows pass. |
| **Level 5** | Full Production Build + Master Harness (`verify_all_skills.sh`) | **Mandatory Gate** | Entire ecosystem compiles, bundles, and passes all verification suites simultaneously. |

---

## 2. Repro-First Bug Protocol & Benchmark Checklist

### Bug Fixes
1. Capture a failing test or exact command output showing the defect *before* editing production code.
2. Apply the minimal root-cause fix.
3. Re-run the exact reproduction check and verify it passes without relaxing assertions.

### Explain the Number (`benchmark-checklist`)
Before reporting any latency, bundle size, FPS, or token metric:
- **Baseline vs After**: Measured on identical inputs and hardware.
- **Artifact Check**: Confirm gains did not come from warm cache, skipped validation, or smaller test fixtures.
- **Variance**: Report `N` runs and `p50`/`p95` rather than a single cherry-picked sample.

---

## 3. Honest Disclosure & Documentation Impact Contract

1. **Evidence Tags**: Mark observed tool outputs `[measured]`, code-derived deductions `[inferred]`, and unverified hypotheses `[guess]`.
2. **Unverified Surfaces**: Explicitly disclose any check that could not run locally (e.g., native iOS hardware, live external API credentials) and the residual risk.
3. **Documentation Impact**: Every commit/PR must state either the exact docs updated or `Documentation impact: none — <technical reason>`.
