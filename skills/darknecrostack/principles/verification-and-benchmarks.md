# Verification & Benchmark Principles

Read these principles before debugging, writing tests, reporting benchmark numbers, or claiming completion.

---

## 1. Prove It Works
- **When it applies**: After every implementation, fix, or refactor, before reporting done.
- **Rule**: Verify against the real running artifact — never a proxy, mock stub, or `"it compiles / lints clean"`. Run the real test suite, CLI command, server endpoint, asset validator, or browser/DOM check and inspect full output.
- **Unverified Disclosure**: If a target runtime cannot be executed locally, explicitly state what remains unverified and why.

## 2. Fix Root Causes
- **When it applies**: Debugging bugs, flaky tests, race conditions, or layout overflows.
- **Rule**: Trace the symptom backward to the earliest point where the invariant broke and fix it there. Null-guards or `try/catch` fallbacks at downstream call sites are valid *only* when the incoming state is legitimately optional.

## 3. Sequence Work into Verifiable Units
- **When it applies**: Multi-step migrations, sweeping refactors, or stacking commits and PRs.
- **Rule**: Break work into small units that each end in a runnable check (`pytest`, `tsc`, `skill_linter.py`, `verify_all_skills.sh`). Verify each unit green before starting the next, and order commits so the PR tells a self-proving story under 1,000 lines per commit.

## 4. Test Behavior, Not Implementation
- **When it applies**: Authoring or updating unit, integration, or E2E tests.
- **Rule**: Assert observable outcomes through public contracts and accessible user locators (`getByRole`, `getByLabel`, HTTP status + persisted DB state), never private helper internals, CSS class names, or call-count mocks that survive broken behavior.

## 5. Explain the Number (`benchmark-checklist`)
- **When it applies**: Before trusting, reporting, or acting on any measured metric (speedup, token savings, bundle size, LCP/INP, throughput, eval score).
- **Mandatory Checklist**:
  1. **Baseline & Sample Size**: State baseline vs. after on identical hardware/inputs (`N`, median + p95, not cherry-picked best run).
  2. **Bottleneck Identification**: Identify what actually limited the number (CPU, I/O, lock contention, GC, layout thrash).
  3. **Artifact Exclusion**: Rule out warm-cache bias, skipped work, test-fixture shrinkage, or measuring the wrong code path.
  4. **Label**: Report numbers as `[measured]` with exact command, or `[inferred]` if analytically estimated.
