# Playbook: Metric Hillclimbing (`hillclimb`)

Use when iteratively optimizing an eval score, Lighthouse/CWV score, token budget, bundle size, or model accuracy.

## Steps
1. **Freeze Eval Harness**: Lock the benchmark dataset, scoring script, and hardware/environment parameters before iteration 1.
2. **Record Baseline**: Log `iter=0` metric in `.agents/memory/decision_trail.tsv` via `log_decision_trail.py`.
3. **Single-Hypothesis Iterations**: Change one clear lever per round (`Build the Lever`), measure after each, and immediately revert any change that regresses quality or fails correctness tests.
4. **Explain Every Delta**: Apply `benchmark-checklist` (`Explain the Number`) to confirm gains are real and not skipped work or cache warmth.
5. **Stop Condition**: Halt at target threshold or diminishing returns (`<1%` gain over 2 consecutive iterations) and ship the cleanest minimal winner.
