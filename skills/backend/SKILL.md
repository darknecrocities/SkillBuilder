---
name: backend
description: Architect, implement, and maintain resilient backend services, clean architecture, REST/gRPC API contracts, strict schema validation, authentication, rate-limiting, and error handling.
---

# Backend Systems Engineering (`/backend`)

> **Role**: Principal Backend & Distributed Systems Architect  
> **Philosophy**: *Domain logic in the core. Validate at the boundaries. Enforce idempotency. Never make unbounded calls.*

This skill establishes backend engineering discipline across microservices, REST APIs, GraphQL, and gRPC systems. It enforces clean architecture separation, strict runtime schema validation (Zod, Pydantic v2), defense-in-depth authentication, and structured RFC 7807 error handling.

---

## 1. Quick Navigation & Progressive Disclosure

| Resource Type | Document | Description |
| :--- | :--- | :--- |
| **Reference** | [references/api-design-and-contracts.md](references/api-design-and-contracts.md) | RESTful conventions, route verbs, cursor pagination, OpenAPI 3.1. |
| **Reference** | [references/validation-and-type-safety.md](references/validation-and-type-safety.md) | Zod / Pydantic v2 boundary validation, custom coercions, fail-fast rules. |
| **Reference** | [references/auth-and-access-control.md](references/auth-and-access-control.md) | JWT rotation, secure cookies, refresh tokens, RBAC, OAuth2/OIDC. |
| **Reference** | [references/resilience-and-middleware.md](references/resilience-and-middleware.md) | Idempotency keys, rate limiters, timeout deadlines, circuit breakers. |
| **Reference** | [references/backend-error-catalog.md](references/backend-error-catalog.md) | Backend error catalog: unhandled rejections, race conditions, timeouts. |
| **Template** | [templates/api_route_template.ts](templates/api_route_template.ts) | Production TypeScript API route with Zod validation and error boundary. |
| **Template** | [templates/domain_service_template.py](templates/domain_service_template.py) | Clean architecture Python service layer with domain exceptions. |
| **Utility** | [scripts/verify_api_contracts.py](scripts/verify_api_contracts.py) | CLI auditor verifying validation schemas and status code compliance. |

---

## 2. Core Backend Invariants

### 1. Clean Architecture Layer Separation
- **Domain Layer**: Pure business entities, value objects, and domain exceptions. Zero framework imports.
- **Service Layer**: Application orchestrator, transaction boundaries, idempotency checks.
- **Repository Layer**: Concrete database access (Prisma, Drizzle, SQLAlchemy).
- **Transport / Controller Layer**: HTTP / gRPC handlers, serialization, and status code mapping.

### 2. Boundary Validation (Fail Fast)
- Every incoming request payload, query string, and route param must be validated using a strict schema before reaching domain services.
- Never pass raw `req.body` directly to database layers.

### 3. RFC 7807 Problem Details
All API errors must return a standardized JSON payload:
```json
{
  "type": "https://api.example.com/errors/validation-error",
  "title": "Invalid Request Parameters",
  "status": 400,
  "detail": "Field 'email' must be a valid email address.",
  "instance": "/api/v1/users",
  "invalid_params": [{ "name": "email", "reason": "malformed format" }]
}
```

### 4. Idempotency & Rate Limiting
- Mutations (`POST`, `PUT`, `DELETE`) with side effects (payments, bookings, notifications) must accept an `Idempotency-Key` header and cache responses in Redis/memory.
- Public endpoints must enforce rate limiting (e.g. 60 requests/minute per IP/user).

---

## 3. Automation Tool: API Contract Verifier

Audit backend route files for validation schemas:
```bash
python3 scripts/verify_api_contracts.py --path src/routes/
```
