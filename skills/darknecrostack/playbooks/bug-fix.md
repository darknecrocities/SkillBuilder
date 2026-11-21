# Playbook: Bug Fix

Use for regressions, runtime errors, broken UI states, or failing tests.

## Steps
1. **Restate Goal**: State the broken behavior and expected contract in one sentence.
2. **Reproduce First**: Write or run a failing test, script, or deterministic command that reproduces the defect *before* modifying production code.
3. **Trace Root Cause**: Work backward from symptom to the earliest invariant violation (`Fix Root Causes`, never slap downstream null-guards on broken upstream state).
4. **2-Strike Circuit Breaker (`Attack the Premise`)**: If 2 fixes sharing the same assumption fail the reproduction check, stop patching. Write the hidden premise down and run a direct diagnostic probe to verify/falsify it.
5. **Apply Minimal Fix**: Change the smallest surface area needed (`Laziness Protocol`).
6. **Prove It Works**: Re-run the reproduction test (now passing), related regression suite, and line/slop checks.
