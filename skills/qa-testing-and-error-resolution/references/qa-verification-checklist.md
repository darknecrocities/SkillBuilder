# Pre-Flight QA Verification Checklist

Before declaring any coding or refactoring task complete, execute this audit checklist:

---

## 1. Static Quality Gates
- [ ] **Physical Line Limit**: All source files maintain <= 500 physical lines (`python3 check_source_line_limits.py`).
- [ ] **Type Safety**: Zero compiler warnings or errors (`tsc --noEmit`, `mypy`, `pyright`, `go vet`).
- [ ] **Linter & Formatting**: Zero linting failures (`eslint`, `ruff check`, `golangci-lint`).

## 2. Dynamic & Test Quality Gates
- [ ] **Unit Tests**: All unit tests pass with 100% determinism.
- [ ] **Integration Tests**: Tested against real persistence (SQLite/PostgreSQL) with zero mock arrays.
- [ ] **Negative & Edge Cases**: Verified behavior under empty input, malformed input, network timeouts, and duplicate submissions.

## 3. Security & Operational Gates
- [ ] **Secrets & Env**: Zero raw credentials in Git. `.env.example` updated with all required keys.
- [ ] **Resilience**: Outbound network requests configure explicit timeouts (3s/15s) and retry backoff.
- [ ] **Error Logging**: All errors caught and structured; no unhandled promise rejections.
- [ ] **LaE Compliance**: Any encountered bug is recorded with root cause and regression test.
