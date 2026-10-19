# Feature Specification Template (Token-Efficient)

**Objective**: [1 concise sentence describing the end state]
**Scope**: [Components affected, e.g. Frontend UI, API Endpoint, Database Schema]
**Stack Constraints**: [Explicit versions, frameworks, and libraries]

---

## 1. Requirements Matrix

| ID | Requirement Description | Inputs | Expected Output / State |
| :--- | :--- | :--- | :--- |
| FR-1 | [Functional requirement 1] | [Input types/values] | [Exact return/mutation] |
| FR-2 | [Functional requirement 2] | [Input types/values] | [Exact return/mutation] |

---

## 2. API Contract & Schema

```typescript
// Request Payload Schema
interface RequestPayload {
  // explicit typed fields
}

// Response Payload Schema
interface ResponsePayload {
  // explicit typed fields
}
```

---

## 3. Security & Resilience Guardrails
- **Validation**: Schema validation via Zod / Pydantic v2.
- **Timeouts**: Outbound request timeout set to [3s / 15s].
- **Auth**: RBAC / JWT token check required on route.
- **Persistence**: Real database transaction with rollback.

---

## 4. Verification Checklist
- [ ] Static type check passes without errors.
- [ ] Unit tests cover happy path + 2 error states.
- [ ] File adheres to 500-line physical ceiling.
- [ ] Manual test verifies database persistence.
