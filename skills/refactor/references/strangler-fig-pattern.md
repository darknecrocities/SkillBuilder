# Strangler Fig & Branch-by-Abstraction Decomposition Manual

> **Objective**: Decompose monolithic 500+ line files and migrate high-risk subsystems incrementally with zero downtime and instant rollback.

---

## 1. The 5-Stage Strangler Fig Execution Sequence

1. **Define Narrow Seam Interface**: Extract an explicit TypeScript interface or Python `Protocol` capturing only what callers actually need (`PaymentGateway`, `SearchEngine`).
2. **Wrap Legacy Behind Adapter**: Place the existing legacy module behind the interface without changing runtime behavior. Run all tests green.
3. **Build New Cohesive Modules**: Implement clean domain slices (`<= 250–350` lines each) behind the interface with full unit tests.
4. **Cut Over Incrementally**: Switch callers cleanly (or via deterministic feature toggle/shadow comparison on high-risk paths), verifying parity on every cutover unit.
5. **Subtract Legacy & Re-Exports**: Delete the deprecated implementation and temporary adapter in one clean wave (`Migrate Callers Then Delete Legacy APIs`).

---

## 2. Cohesive File-Split Rules (Anti-Shotgun Surgery)

Never slice a 600-line file randomly at line 300 just to satisfy `check_source_line_limits.py`. Split strictly along domain responsibility seams:

| Mixed Concern Inside God File | Cohesive Extraction Target |
| :--- | :--- |
| **Input Schemas & Types** | `contracts/<domain>Schemas.ts` |
| **SQL / Storage Queries** | `repositories/<domain>Repository.ts` |
| **Pure Calculations / State Machine** | `domain/<domain>Engine.ts` |
| **React JSX Subviews & Hooks** | `components/<Feature>Header.tsx`, `hooks/use<Feature>.ts` |

Verify after splitting: `python3 skills/world-class-engineering/scripts/check_source_line_limits.py --path . --show-tiers`.
