# Polished Engineering Specification

## 1. Intent & Scope
- **Objective**: [Concise single sentence]
- **Target Tier**: [Frontend | Backend | Database | Cloud | Fullstack]
- **Target Files / Boundaries**: [file:///path/to/target]

## 2. Technical Contracts & Invariants

```typescript
// Core Data Contract
export interface EntityContract {
  id: string;
  createdAt: string;
}
```

## 3. Boundary & Error Invariants
- **Validation**: Schema-level validation on all inputs.
- **Resilience**: Explicit 3s connection timeout and 15s execution timeout.
- **Failure States**: Return RFC 7807 problem details on any error.

## 4. Verification Gate
- [ ] Unit tests pass: `npm test` or `pytest`.
- [ ] Type check passes: `tsc --noEmit` or `mypy`.
- [ ] File size complies with 500-line ceiling: `check_source_line_limits.py`.
