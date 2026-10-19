# Bug Reproduction & Resolution Spec

**Bug ID**: [BUG-YYYYMMDD-XX]
**Severity**: [Critical / High / Medium / Low]
**Component**: [Service / Route / UI Component]

---

## 1. Reproduction Steps & Observed Behavior

```bash
# Reproduction Command / Request
curl -X POST http://localhost:8080/api/v1/resource \
  -H "Content-Type: application/json" \
  -d '{"invalid": "field"}'
```

- **Expected**: HTTP 400 Bad Request with RFC 7807 problem details.
- **Observed**: HTTP 500 Internal Server Error (Unhandled exception).
- **Stack Trace / Logs**:
  ```text
  [Paste exact minimal error message and line number]
  ```

---

## 2. Root Cause Analysis
- **Trigger**: [Why the bug triggered under these conditions]
- **Flaw**: [Missing validation / null pointer / race condition]

---

## 3. Concrete Remediation & Test
- [ ] Implement boundary validation or error guard.
- [ ] Write regression test replicating exact reproduction conditions.
- [ ] Run test suite to verify zero regressions.
- [ ] Log entry in Master Error Catalog.
