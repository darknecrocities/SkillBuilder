# Code Review Report: [PR / Branch / Task Name]

> **Reviewer**: [Reviewer Role / Name]  
> **Target Branch**: `main` ← `feature-branch`  
> **Overall Recommendation**: [APPROVE / REQUEST_CHANGES / COMMENT]  

---

## 1. Executive Summary
[Concise 2–3 paragraph summary of the reviewed changes, architecture fit, and overall quality.]

---

## 2. Quality Gate Evaluation

| Quality Gate | Status | Notes |
| :--- | :--- | :--- |
| **Gate 1: Requirements** | [PASS / FAIL / N/A] | Acceptance criteria met. |
| **Gate 2: Architecture** | [PASS / FAIL / N/A] | High cohesion, no circular deps. |
| **Gate 3: Implementation** | [PASS / FAIL / N/A] | Adheres to 500-line source limit. |
| **Gate 4: Correctness** | [PASS / FAIL / N/A] | Automated tests executed and passing. |
| **Gate 5: Security** | [PASS / FAIL / N/A] | Input sanitized, zero committed secrets. |
| **Gate 6: Maintainability** | [PASS / FAIL / N/A] | Clean code, no dead code or duplication. |
| **Gate 7: Delivery** | [PASS / FAIL / N/A] | Verification documented, trade-offs noted. |

---

## 3. Prioritized Findings

### Critical (Blockers — Must Fix)
#### [C-01] [Finding Title: e.g., Unsafe SQL String Concatenation]
- **Location**: `src/repositories/user_repository.ts:48-52`
- **Impact / Failure Scenario**: An attacker passing a malicious string to `searchUsers(query)` can execute arbitrary SQL injection, exposing user tables.
- **Evidence**:
  ```typescript
  const sql = `SELECT * FROM users WHERE name LIKE '%${query}%'`;
  ```
- **Recommended Minimal Fix**:
  ```typescript
  const sql = `SELECT * FROM users WHERE name LIKE $1`;
  return db.query(sql, [`%${query}%`]);
  ```

---

### Major (Should Fix Before Merge)
#### [M-01] [Finding Title: e.g., Source File Exceeds 500-Line Policy]
- **Location**: `src/services/billing_service.ts` (612 lines)
- **Impact / Failure Scenario**: Violates the single-responsibility principle and 500-line architectural guardrail.
- **Evidence**: `scripts/check_source_line_limits.py` reports 612 lines.
- **Recommended Minimal Fix**: Extract tax calculation and PDF rendering into dedicated sibling modules (`tax_calculator.ts` and `invoice_pdf_renderer.ts`).

---

### Minor / Suggestions (Non-Blocking)
#### [N-01] [Finding Title: e.g., Variable Name Clarity]
- **Location**: `src/utils/math.ts:14`
- **Recommendation**: Rename `tmp` to `standardDeviation` to clarify mathematical intent.

---

## 4. Verification Evidence
- **Automated Tests Executed**:
  ```bash
  npm test
  # 42 tests passed, 0 failed
  ```
- **Line Limit Check**:
  ```bash
  python3 scripts/check_source_line_limits.py --path src
  ```
