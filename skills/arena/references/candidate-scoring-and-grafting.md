# Candidate Scoring & Trait-Grafting Manual

> **Objective**: Prevent premature lock-in on hard architectural, algorithmic, or UI design problems by exploring orthogonal alternatives and grafting only proven strengths.

---

## 1. Designing Orthogonal Candidates (Not Cosmetic Clones)

If Candidate A and Candidate B share the same data model, control flow, and layout structure, you have not explored the design space. Force genuine structural contrast:

| Problem Domain | Weak Arena (Avoid) | Strong Arena (Orthogonal Axes) |
| :--- | :--- | :--- |
| **UI Dashboard** | Same 3-card grid with indigo vs zinc colors | A: High-density bento telemetry strip; B: Master-detail split table; C: Command-palette-first workspace |
| **Client Persistence** | `localStorage` key A vs key B | A: Structured `IndexedDB` stores with versioned migrations; B: `OPFS` worker + binary WAL snapshots |
| **Client Search** | Regex loop vs `.includes()` | A: Inverted index (`MiniSearch`) + alias map; B: Normalized trigram index in SQLite-Wasm |
| **2D Mascot Rig** | Two CSS bounce timings | A: Rive `.riv` 6-state interactive machine; B: `<35`-node mathematical SVG rig with pointer pupil tracking |
| **Concurrency** | Mutex vs RWLock on same global map | A: Partitioned per-shard ownership (zero sharing); B: Single-writer actor queue with bounded backpressure |

---

## 2. Weighted Scoring Rubric

Score each candidate `1–5` after prototyping or sketching concrete types/layouts:

| Candidate | Correctness & Edge Cases (30%) | Reader Load & Simplicity (25%) | Latency / Frame / Token Budget (25%) | Reversibility & Blast Radius (20%) | Weighted Total |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Candidate A** | 5 | 4 | 4 | 5 | `4.50` |
| **Candidate B** | 5 | 3 | 5 | 3 | `4.10` |
| **Candidate C** | 4 | 5 | 3 | 4 | `4.00` |

---

## 3. Trait-Grafting Protocol (Zero Frankenstein Bloat)

1. **Pick One Base**: Choose the highest-scoring clean architecture as the foundation. Never splice two incompatible state paradigms together.
2. **Justify Each Graft**: Name the exact weakness in the winning base and the exact minimal trait borrowed from a runner-up (e.g., *"Adopt Candidate B's pre-allocated `Float32Array` buffer inside Candidate A's worker loop"*).
3. **Subtract Throwaway Probes**: Delete losing prototypes from `scratch/` before committing.
4. **Verify After Graft**: Run full unit/integration tests and `check_source_line_limits.py --show-tiers` (`<= 500` lines, `<= 40` lines/func).
