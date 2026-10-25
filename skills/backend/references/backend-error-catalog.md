# Backend & Systems Error Catalog

Defects, race conditions, and failures in backend services and APIs.

---

### [BE-ERR-001] Missing Body Validation Schema (Injection / Malformed Input)
- **Symptom**: Uncaught `TypeError: Cannot read properties of undefined (reading 'toLowerCase')` inside domain service.
- **Root Cause**: Handler assumed incoming JSON structure was valid without schema parsing.
- **Remediation**: Parse body through Zod/Pydantic schema as the first line of the handler. Return HTTP 400 with parameter details on parse failure.

---

### [BE-ERR-002] Race Condition on Concurrent Mutation (Double Spend / Duplicate Record)
- **Symptom**: User rapidly clicks "Submit" twice; two identical database rows are created.
- **Root Cause**: Database read-then-write without unique database constraints or distributed lock / idempotency key.
- **Remediation**:
  1. Add a unique index on composite fields (`tenant_id`, `idempotency_key` or `user_id`, `reference_id`).
  2. Use `INSERT ... ON CONFLICT DO NOTHING` or serializable transactions.

---

### [BE-ERR-003] JWT Algorithm Confusion / Insecure Verification
- **Symptom**: Token parser accepts tokens signed with `none` algorithm or verifies asymmetric RS256 token using public key as HMAC secret.
- **Root Cause**: Not explicitly restricting `algorithms: ['RS256']` in JWT verification options.
- **Remediation**: Explicitly lock the algorithm list in `jwt.verify(token, secret, { algorithms: ['RS256'] })`.
