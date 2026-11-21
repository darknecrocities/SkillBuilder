# Authentication, Refresh Token Rotation & RBAC Manual

> **Objective**: Eliminate session hijacking, timing side-channels, JWT algorithm confusion, and broken object-level authorization (BOLA).

---

## 1. Cryptographic & Cookie Invariants

- **Password Hashing**: Always hash passwords with **Argon2id** (`memory=64MB, iterations=3, parallelism=4`) or **bcrypt** (`cost >= 12`). Never store SHA-256/MD5 password hashes.
- **Constant-Time Secret Comparison**: Compare API keys, HMAC signatures, and CSRF tokens exclusively via `crypto.timingSafeEqual` (Node) or `hmac.compare_digest` (Python).
- **Cookie Flags**: Every session/refresh cookie MUST enforce `HttpOnly; Secure; SameSite=Lax; Path=/` (use `SameSite=Strict` where cross-site link landing is unnecessary).

---

## 2. Refresh Token Family Rotation (Reuse Detection)

1. Issue a short-lived access JWT (`5–15` min, explicit `alg: "EdDSA"` or `"RS256"` — never accept `"none"` or `"HS256"` fallback on asymmetric keys) alongside an opaque refresh token linked to `family_id`.
2. On `/auth/refresh`, mark the presented token `used_at = NOW()` inside a DB transaction and issue its successor in the same `family_id`.
3. **Reuse Detection**: If an already-used token is presented again, immediately revoke **all active tokens in that `family_id`** and force re-authentication.

---

## 3. Tenant-Scoped RBAC & BOLA Prevention

- Never trust `userId` or `tenantId` from request body or query params when deriving authorization; read strictly from the verified session/token claims.
- Combine route-level role checks (`requireRole("admin")`) with row-level query predicates (`WHERE resource_id = $1 AND tenant_id = $2`).
