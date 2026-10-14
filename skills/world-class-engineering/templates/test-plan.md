# Test Strategy & Verification Plan: [Feature/Component Name]

> **Scope**: [e.g., Auth Service & JWT Refresh Workflow]  
> **Author**: [Test Engineer / Agent]  
> **Status**: [Draft / Ready / Executed]  

---

## 1. Testing Objectives
[Define what behaviors, edge cases, contracts, and failure modes are being verified.]

---

## 2. Test Matrix

| ID | Test Category | Target Component | Scenario & Input | Expected Outcome | Verification Tool / Command |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T-01** | Unit | `TokenValidator` | Expired token provided | Throws `TokenExpiredError` | `pytest tests/unit/test_tokens.py` |
| **T-02** | Unit | `TokenValidator` | Tampered signature | Throws `InvalidSignatureError` | `pytest tests/unit/test_tokens.py` |
| **T-03** | Integration | `POST /auth/refresh` | Valid refresh token in cookie | Returns 200 with new JWT | `npm test -- tests/integration/auth.test.ts` |
| **T-04** | Security | `POST /auth/refresh` | Replay revoked refresh token | Returns 401 and invalidates family | `npm test -- tests/security/replay.test.ts` |
| **T-05** | Performance | `TokenValidator` | 1,000 concurrent validations | p99 latency < 5ms, 0 memory leak | `k6 run tests/perf/token_benchmark.js` |

---

## 3. Fixtures, Stubs, & Mocking Strategy
- **Deterministic Clocks**: Mock time to verify token expiration without waiting real seconds.
- **External IdP Mock**: Use local mock server for OAuth2 provider callbacks.
- **Database Isolation**: Wrap all database test suites in rollback transactions.

---

## 4. Execution Commands & Automation
```bash
# 1. Run unit test suite
pytest tests/unit -v

# 2. Run integration tests against test container
pytest tests/integration -v

# 3. Check for 500-line compliance on test files
python3 scripts/check_source_line_limits.py --path tests
```
