# Core Principles: Execution & Levers

Read these principles when planning migrations, evaluating UX trade-offs, exploring novel designs, or automating repetitive tasks.

---

## 1. Outcome-Oriented Execution
- **When it applies**: Planned rewrites, schema migrations, and multi-phase updates with explicit boundaries.
- **Rule**: Converge cleanly on the target architecture. Do not preserve throwaway compatibility shims or half-migrated dual paths unless a zero-downtime expand/contract rollout explicitly requires a temporary window with a deletion milestone.
- **Litmus Test**: Every phase ends with a cleaner, unified system — not two legacy systems stitched together.

## 2. Experience First
- **When it applies**: Product, UI/UX, mascot interaction, latency, or feature-scope trade-offs.
- **Rule**: Choose user delight, clarity, and responsiveness over implementation convenience. Three razor-sharp, spring-tuned, zero-CLS features beat ten half-baked controls.
- **Litmus Test**: Reject "good enough for a developer" defaults (raw JSON dumps, jittery loading layouts, emoji buttons, frozen main threads during media processing).

## 3. Exhaust the Design Space
- **When it applies**: Novel interactions, ambiguous architectures, or high-impact algorithms with no clear precedent in the codebase.
- **Rule**: Build or sketch 2–3 genuinely competing prototypes (via `/arena` or `playbooks/prototype.md`) with distinct shapes/layouts/structures and compare them against explicit criteria before locking one in.
- **Litmus Test**: Your first plausible design is rarely the global optimum.

## 4. Build the Lever
- **When it applies**: Repetitive multi-file migrations, asset matrix generation, audit sweeps, or verification checks.
- **Rule**: Build the deterministic tool (script, codemod, generator, linter) that executes or proves the change, rather than doing 30 manual edits by hand. The tool becomes a permanent, rerunnable artifact for reviewers and CI.
- **Litmus Test**: If a reviewer asks *"how do I know all 48 skills/files match?"*, point to the executable lever you built and ran.
