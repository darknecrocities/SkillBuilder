<!-- ======================================================================= -->
<!-- Standard Pull Request Template (Ready-to-Review)                        -->
<!-- Use this structure whenever preparing a PR for user review.             -->
<!-- ======================================================================= -->

# PR: <type>(<scope>): <Clear imperative title>

> **Author**: [Agent / Engineer Name]  
> **Source Branch**: `feat/<branch-name>` → **Target Branch**: `main`  
> **Diff Estimate**: [e.g., +412 lines / -85 lines across 6 files]  

---

## 1. Summary & Objective
[Provide a concise 1-2 paragraph description of what this PR does, why it is needed, and what business/technical problem it resolves.]

---

## 2. Key Architectural Decisions & Trade-Offs
- **Decision 1**: [Description and rationale]
- **Decision 2**: [Description and rationale]
- **Trade-Off**: [Any trade-off made, e.g. using memory cache over Redis for initial simplicity]

---

## 3. Files Changed
| Status | File Path | Cohesive Responsibility |
| :--- | :--- | :--- |
| `[NEW]` | `src/modules/billing/invoice_calculator.ts` | Pure domain calculation logic (< 200 lines). |
| `[NEW]` | `tests/unit/invoice_calculator.test.ts` | Unit tests covering tax brackets and zero values. |
| `[MODIFY]` | `src/routes/billing_routes.ts` | Wire new invoice creation endpoint. |

---

## 4. Verification & Testing Evidence

### Automated Test Results
```bash
$ npm test
PASS src/modules/billing/invoice_calculator.test.ts
  ✓ calculates zero tax for exempt items (2 ms)
  ✓ applies standard 10% tax rate correctly (1 ms)
  ✓ rounds fractional cents up to nearest integer (1 ms)

Test Suites: 1 passed, 1 total
Tests:       3 passed, 3 total
Snapshots:   0 total
Time:        0.842 s
```

### Static Analysis & Line-Limit Audit
```bash
$ python3 scripts/check_source_line_limits.py --path src
[PASS] All checked source files comply with the 500-line guardrail.
```

---

## 5. Configuration, Environment, & Migrations
- [ ] **Environment Variables**: Added new keys to `.env.example`.
- [ ] **Database Migrations**: [Yes / No / Migration file name]
- [ ] **Breaking Changes**: [None / Documented breaking change]

---

## 6. Rollback / Emergency Recovery Plan
[State the exact steps required to rollback this deployment if unexpected errors occur in production.]
- Command: `git revert <commit-sha> && git push origin main`
- Rollback migration: `npm run migration:rollback`
