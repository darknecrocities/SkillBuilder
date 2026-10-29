# Characterization Testing for Safe Refactoring

Characterization tests pin down existing actual behavior—bugs and quirks included—to create a safety net before refactoring code.

---

## 1. Test Authoring Protocol

1. Exercise the existing function across standard, edge-case, and boundary inputs.
2. Record the exact outputs produced by the system.
3. Assert those exact outputs in an automated test suite.
4. Execute tests before making any edits: verify green.
5. Apply structural decomposition.
6. Re-run tests: if any assertion fails, a regression occurred.
