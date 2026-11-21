# Playbook: Performance Investigation (`perf-issue`)

Use when diagnosing slow endpoints, high memory usage, bundle bloat, N+1 queries, or dropped UI frames.

## Steps
1. **Define Target Metric & Baseline**: Measure baseline latency (`p50`/`p95`), memory RSS, frame time, or bundle KB on reproducible inputs (`Explain the Number`).
2. **Isolate the Bottleneck**: Profile CPU/flamegraph, SQL `EXPLAIN ANALYZE`, network waterfall, or React/Flutter frame timeline before touching code.
3. **Rank Hypotheses**: List top 2–3 bottlenecks by expected impact vs implementation cost.
4. **Optimize One Variable at a Time**: Fix root cause (batch N+1 queries, move heavy Canvas/WASM to Worker, clamp 3D DPR `<=2`, memoize hot selectors).
5. **Verify Without Bias**: Re-measure with identical cold/warm conditions, sample count `N`, and check correctness tests still pass.
