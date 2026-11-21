# TDD Red-Green-Refactor & MSW Network Contract Testing

> **Objective**: Ensure every feature and bugfix is backed by isolated, fast, behavior-driven tests using real persistence or HTTP-layer MSW interception.

---

## 1. The TDD Cycle & Repro-First Bug Rule

1. **Red**: Write a failing test asserting the required behavior or reproducing the exact bug *before* touching production code. Confirm the test fails for the expected reason.
2. **Green**: Write the smallest clean production implementation needed to pass (`Laziness Protocol`).
3. **Refactor**: Eliminate duplication, enforce `<= 40` lines/func and `<= 3` nesting, and verify tests remain green.

---

## 2. Mock Service Worker (MSW) vs. Internal Method Stubs

- **Avoid Fragile Internal Stubs**: Stubbing `vi.spyOn(service, "_formatRow")` tests internal wiring rather than real behavior — tests stay green even when serialization or HTTP parsing breaks.
- **Intercept at the HTTP Boundary (MSW)**: When testing clients talking to external third-party APIs, mount MSW handlers (`onUnhandledRequest: "error"`) so real `fetch`, headers, timeouts, and error status codes (`400`, `429`, `500`) run end-to-end.
- **Real Local DB for Persistence Tests**: Test repositories against ephemeral SQLite `:memory:` or isolated test transactions rolled back per test (`Test Behavior, Not Implementation`).

---

## 3. Test Isolation & Hygiene Rules
- Zero shared mutable globals across `it(...)` blocks; run tests with clean per-test fixtures (`beforeEach` / `TemporaryDirectory`).
- Never skip failing tests (`it.skip`, `@unittest.skip`) or weaken assertions just to make CI green.
