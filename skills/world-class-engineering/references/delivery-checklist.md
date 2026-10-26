# Delivery and Quality Gates Checklist

This checklist must be audited and verified before declaring any non-trivial engineering task, pull request, or delivery complete.

---

## The 7 Quality Gates Audit

### Gate 1: Requirements & Acceptance Criteria
- [ ] Every explicit requirement from the user prompt or specification is implemented.
- [ ] Core input, output, and error conditions have been verified.
- [ ] All stated assumptions have been disclosed.

### Gate 2: Architecture & Boundaries
- [ ] Modules exhibit high cohesion and loose coupling.
- [ ] Domain business logic is cleanly isolated from infrastructure, web frameworks, and persistence.
- [ ] No circular dependencies exist across packages or modules.
- [ ] Any introduced dependency is strictly necessary and justified.

### Gate 3: Implementation & Multi-Tiered Line Policy
- [ ] All modified and newly created source files adhere to the **500-line physical limit** and target the **150–250 line sweet spot**.
- [ ] No functions exceed 40 physical lines; nesting depth stays within $\le 3$ levels with early return guard clauses.
- [ ] Verification script has been executed:
  ```bash
  python3 skills/world-class-engineering/scripts/check_source_line_limits.py --path . --show-tiers
  ```
- [ ] Variable and function names clearly communicate domain intent.
- [ ] No dead, unreachable, or commented-out code remains.

### Gate 4: Correctness & Verification
- [ ] Automated unit and integration tests have been executed.
- [ ] Test command results have been empirically inspected (not assumed).
- [ ] All tests pass cleanly with zero unresolved failures.
- [ ] Static type checking (`tsc`, `mypy`, `pyright`, `go vet`, `cargo check`) passes with zero errors.
- [ ] Linters and formatters report zero violations.

### Gate 5: Security & Privacy
- [ ] All inputs at system boundaries are validated against strict schemas.
- [ ] Zero secrets, API keys, credentials, or private keys are committed.
- [ ] All database queries use parameterized statements; no raw SQL string concatenation.
- [ ] File operations and shell invocations are secured against path traversal and command injection.
- [ ] Least privilege is maintained across permissions and API scopes.

### Gate 6: Maintainability & Cleanliness
- [ ] No duplicate business logic or boilerplate has been copied across files.
- [ ] No speculative, unused abstractions or "future-proofing" frameworks have been added.
- [ ] Unrelated user files and configurations remain untouched.

### Gate 7: Delivery & Reporting
- [ ] A concise, transparent summary of changed files is prepared.
- [ ] Commits adhere to the 1,000-line budget with **mandatory Conventional Title AND structured Description body**.
- [ ] All commits are pushed to the remote branch (`git push origin <branch>`) with working tree clean.
- [ ] Active, ready-to-merge GitHub Pull Request authored or updated (`gh pr create` / `gh pr edit`).
- [ ] Exact verification commands and test execution results are documented.
- [ ] Any required configuration changes, new environment variables, or migration steps are clearly noted.
- [ ] Known edge cases, trade-offs, or remaining limitations are honestly reported.
