# Strangler Fig Refactoring Pattern

Safely decompose large monolithic files or legacy modules without downtime or risky rewrite attempts.

---

## 1. Strangler Fig Phased Execution

```text
Step 1: Intercept incoming calls via a facade or interface
Step 2: Implement new cohesive domain slice (150–250 lines)
Step 3: Route 10% -> 50% -> 100% of calls to the new slice
Step 4: Deprecate and delete old branch in the monolith
```

---

## 2. Guardrails Against Regressions

1. Never alter business logic while decomposing files; refactor structure first, verify tests, then optimize logic.
2. Maintain characterization test coverage across all boundary interfaces before touching source code.
3. Keep individual commits bounded under 500 lines of net change.
