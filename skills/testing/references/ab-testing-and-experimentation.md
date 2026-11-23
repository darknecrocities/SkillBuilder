# Controlled A/B Testing, Experimentation & Statistical Verification

> **Objective**: Eliminate p-hacking, Sample Ratio Mismatch (SRM), hydration flicker, and unmeasured feature/AI rollouts with deterministic hash bucketing and pre-registered statistical gates.

---

## 1. Experiment Contract & Pre-Registration Checklist

Before shipping any A/B, A/B/n, or AI model/prompt experiment, lock these five parameters:

| Field | Requirement | Example |
| :--- | :--- | :--- |
| **Primary Metric (OEC)** | Single North-Star conversion or quality metric | Checkout completion rate (`+1.5%` absolute lift) |
| **Guardrail Metrics** | Non-negotiable regression ceilings | `p95_latency_ms <= +15ms`, `error_5xx < 0.5%`, `crash_free >= 99.9%` |
| **Statistical Power & Alpha** | Fixed before launch; zero post-hoc threshold edits | `alpha = 0.05` (two-sided), `power (1 - beta) >= 0.80`, `MDE = 2.0%` |
| **Unit of Randomization** | Consistent entity across the entire funnel | `user_id` (logged-in) or `anon_session_id` (funnel); never mix per-request |
| **Exposure Boundary** | Log `experiment_exposed` ONLY when user hits the divergent branch | Prevents dilution from ineligible visitors (`90%` unexposed noise) |

---

## 2. Deterministic Hash Bucketing (Zero Flicker / SSR-CSR Parity)

Never use `Math.random()`, `random.random()`, or mutable client-only cookies to assign variants—random assignment breaks repeat-visit consistency and causes React/Next.js SSR hydration flicker. Hash `"{experiment_id}:{salt}:{subject_id}"` into `[0, 10000)`:

```python
import hashlib


def assign_bucket(subject_id: str, experiment_id: str, salt: str, split_bps: int = 5000) -> str:
    """Deterministically assign 'control' or 'treatment' via SHA-256 basis points (0..9999)."""
    digest = hashlib.sha256(f"{experiment_id}:{salt}:{subject_id}".encode("utf-8")).digest()
    bucket = int.from_bytes(digest[:4], "big") % 10000
    return "treatment" if bucket < split_bps else "control"
```

- **A/A Calibration First**: On new experiment infrastructure, run a `50/50` A/A dry run (`48h` or `>= 5,000` subjects) and verify false-positive rate `~5%` and SRM `p >= 0.001`.
- **Mutual Exclusion Layers**: Orthogonal experiments share different `salt` values; conflicting UI experiments share one exclusivity layer (`hash(layer_id + subject_id)`) so slots never overlap.

---

## 3. Sample Ratio Mismatch (SRM), Peeking & Multi-Variant Guards

1. **Sample Ratio Mismatch (SRM Gate)**: Always run a Pearson chi-squared goodness-of-fit test on observed `(n_control, n_treatment)` vs expected split (`50/50`, `90/10`) *before* reading conversion metrics. If `p_srm < 0.001`, **HALT and discard results**—telemetry loss, bot filtering skew, or caching bugs invalidated randomization.
2. **No Fixed-Horizon Peeking**: Calling a test early when `p < 0.05` on day 2 inflates false positives from `5%` to `25–40%`. Either lock sample size `N` upfront via MDE calculation OR use **Sequential Testing** (mSPRT / O'Brien-Fleming alpha spending).
3. **Multiple Comparisons (A/B/n)**: When testing `k >= 2` treatment arms or `m` secondary metrics, apply **Benjamini-Hochberg (FDR)** or **Bonferroni** ($\alpha_{\text{adj}} = \alpha / m$).
4. **Variance Reduction (CUPED)**: Adjust post-experiment outcomes using pre-experiment covariate $X_{\text{pre}}$ ($Y_{\text{cuped}} = Y - \theta (X_{\text{pre}} - \bar{X})$) to shrink confidence intervals by `20–45%`.

---

## 4. AI / CV / VLM / Local LLM Model Experimentation

When comparing models (`Qwen2.5-VL` vs `Gemini`, `Q4_K_M` vs `Q5_K_M`, or prompt variants):
- **Offline Paired Golden Eval First**: Run both variants on the exact same frozen `N >= 200` stratified dataset using **McNemar's test** (binary pass/fail) or paired bootstrap before live traffic.
- **Shadow / Canary Traffic**: Mirror `5–10%` of production requests asynchronously to the challenger model, measuring `p95 latency`, `tokens_per_request`, `JSON schema parse failure %`, and guardrail safety flags with zero user impact.
- **Post-Experiment Cleanup**: Every shipped or killed experiment flag MUST have a scheduled sunset ticket removing dead branches and retiring the salt within `14` days of decision.
