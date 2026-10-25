# Backend Resilience & Middleware Architecture

Patterns for preventing cascading service failures, enforcing idempotency, and handling rate limits.

---

## 1. Idempotency Key Pattern
For critical mutating endpoints (e.g. `/api/v1/payments`), accept `Idempotency-Key`:

1. Check Redis for key `idempotency:<user_id>:<key>`.
2. If state is `PENDING`, return `409 Conflict` (request currently processing).
3. If state is `COMPLETED`, return the cached response payload immediately.
4. If not found, set state `PENDING` with 60s TTL, process the transaction, and save response payload with 24h TTL.

---

## 2. Circuit Breaker Configuration
When calling third-party APIs (Stripe, Twilio, OpenAI, Gemini):
- **Failure Threshold**: 5 consecutive errors or >50% failure rate over 10s.
- **State Transition**: `CLOSED` -> `OPEN` (fail fast immediately without sending network requests).
- **Cool-Down**: 30s in `OPEN`, then enter `HALF-OPEN` testing single canary requests.
