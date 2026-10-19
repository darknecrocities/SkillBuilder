# Testing Methodology & Quality Engineering

A rigorous approach to testing software systems across unit, integration, and contract layers.

---

## 1. Unit Testing Standards
- **Isolation**: Test pure functions, algorithmic transformations, and domain models without external I/O.
- **Determinism**: Avoid reliance on wall-clock time (`Date.now()`), random numbers, or external network calls. Inject clocks or seeds where needed.
- **Negative Testing**: Every unit test suite must test:
  - Boundary minimums and maximums (empty string, 0, null, max integer).
  - Malformed inputs (unsupported formats, missing required keys).
  - Explicit error throwing and domain exception types.

---

## 2. Integration Testing Standards
- **Real Infrastructure**: Test against real databases (SQLite in memory/file, Docker PostgreSQL container) rather than mock arrays.
- **Transactional Clean-Up**: Roll back transactions after each test run to ensure pristine state.
- **Contract Verification**: Validate that API responses strictly match their OpenAPI or JSON Schema declarations.

---

## 3. End-to-End (E2E) Testing
- Focus exclusively on critical revenue and operational paths:
  - User onboarding & login.
  - Core transaction / checkout / data save flow.
  - Critical export or reporting flow.
- Keep tests resilient to cosmetic UI changes by querying accessible role names (`getByRole('button', { name: /submit/i })`).
