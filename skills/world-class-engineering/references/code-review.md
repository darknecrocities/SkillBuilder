# Code Review and Refactoring Standards

This guide outlines the rubric and methodology for conducting rigorous, evidence-backed code reviews and disciplined refactoring.

---

## 1. The Skeptical Senior Engineer Rubric

Review code with high skepticism and rigorous attention to detail. Evaluate and prioritize all review findings strictly in this order:

```text
Priority 1: Correctness & Data Integrity
      ↓
Priority 2: Security & Privacy
      ↓
Priority 3: Breaking Changes & Compatibility
      ↓
Priority 4: Reliability & Error Handling
      ↓
Priority 5: Performance & Resource Usage
      ↓
Priority 6: Maintainability & Architecture (including 500-line rule)
      ↓
Priority 7: Readability & Style Conventions
```

### Finding Classifications

- **CRITICAL (Blocker)**:
  - Data corruption risk, race condition in financial/transaction logic.
  - Security vulnerability (injection, unauthenticated endpoint, secrets committed).
  - Unintended breaking change to public API contracts.
- **MAJOR (Must Fix Before Merge)**:
  - Unhandled error cases, missing database indexes on queried columns.
  - Memory leak, unclosed database connection or file handle.
  - Violation of the 500-line source file policy without an architectural justification.
- **MINOR (Improvement / Nit)**:
  - Code style inconsistency, minor naming improvements, missing docstrings.
  - Must not block release unless it directly impairs readability or maintainability.

---

## 2. Anatomy of an Actionable Finding

When reporting a code review issue, always provide four concrete elements:

1. **Specific Location**: File path and line number range.
2. **Impact & Failure Scenario**: Exactly what failure occurs under what conditions (e.g., *"If two concurrent requests occur within 5ms, balance updates can overwrite each other"*).
3. **Evidence**: Reference the specific code or test output demonstrating the defect.
4. **Minimal Fix**: Provide a concise diff or concrete recommendation to resolve the issue.

*Negative Example*: *"This looks slow, maybe rewrite it."* (Vague, ungrounded, unhelpful).  
*Positive Example*: *"In `fetchUserOrders` (line 42), the loop triggers an N+1 query by querying `OrderItems` inside the iteration. For a user with 50 orders, this executes 51 SQL queries. Recommend using `include: { items: true }` or a batch join."*

---

## 3. Disciplined Refactoring Protocol

When refactoring existing code:

- **Baseline First**: Before modifying existing logic, ensure test coverage exists for the current behavior. If tests are absent, write characterization tests first.
- **Incremental Steps**: Never execute a massive, multi-file refactor in one step. Make small, isolated changes (extract method, rename symbol, extract class).
- **Preserve Public Contracts**: Keep public method signatures and return types unchanged. Use the Deprecation pattern if a signature must be phased out.
- **Test After Every Step**: Execute the test suite after each atomic refactor step to catch regressions instantly.
- **Preserve Working Systems**: Do not rewrite functioning, battle-tested code solely to align with personal stylistic preferences or newer hype frameworks.
