# Application-Layer DDoS Mitigation, Rate Limiting & Resource Starvation Defense

> **Philosophy**: *Unbounded resources are vulnerabilities. Every HTTP connection, database query, regex evaluation, and JSON payload consumes finite CPU and memory. Defense in depth demands strict caps, sliding-window rate limiting, and defensive timeouts.*

---

## 1. Rate Limiting Architectures & Standard Tiers

Application-layer Distributed Denial of Service (L7 DDoS) exhausts server worker threads, database connections, or memory without triggering network-layer volumetric alerts.

### 1.1 Multi-Tier Rate Limiting Matrix

| Endpoint Tier | Target | Window | Burst Limit | Remediation Action |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1: Public Auth** | IP Address | 1 minute | 5–10 requests | 429 + Exponential Backoff |
| **Tier 2: Authenticated API** | User / Tenant ID | 1 minute | 100–300 requests | 429 + RFC 6585 Headers |
| **Tier 3: Public Read APIs** | IP Address | 1 minute | 60 requests | 429 + Caching Headers |
| **Tier 4: Heavy Compute / Export** | Tenant ID | 10 minutes | 5 requests | Queue Job + 202 Accepted |

### 1.2 RFC 6585 Standard Response Headers
When rate limits are exceeded, return HTTP `429 Too Many Requests` with RFC 6585 / IETF draft headers:

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/problem+json
Retry-After: 45
RateLimit-Limit: 100
RateLimit-Remaining: 0
RateLimit-Reset: 1714089645

{
  "type": "https://errors.skillbuilder.io/rate-limit-exceeded",
  "title": "Too Many Requests",
  "status": 429,
  "detail": "Rate limit quota exceeded. Retry in 45 seconds.",
  "retryAfter": 45
}
```

---

## 2. Slowloris & Connection Starvation Defense

Slowloris attacks hold HTTP connections open indefinitely by sending headers or body chunks at fractions of a byte per second, depleting thread pools.

### Defensive Invariants:
1. **Connection Timeout**: Terminate idle TCP handshakes after **3 seconds**.
2. **Body Read Timeout**: Complete HTTP body reception within **15 seconds**.
3. **Keep-Alive Ceiling**: Cap idle keep-alive sockets at **5 seconds** and limit max requests per socket.

```typescript
// Node.js HTTP Server Configuration
import http from "node:http";

const server = http.createServer(app);

// Close connections that take longer than 15s to transmit headers/body
server.headersTimeout = 5000;
server.requestTimeout = 15000;
server.keepAliveTimeout = 5000;
server.maxHeadersCount = 100;
```

---

## 3. Request Payload & Memory Limits

Unrestricted payload sizes allow memory exhaustion via multi-megabyte JSON trees.

```typescript
// Express / Fastify body parser configuration
app.use(express.json({ limit: "100kb" }));
app.use(express.urlencoded({ extended: true, limit: "100kb" }));
```

- **File Uploads**: Restrict multipart uploads with strict streaming limits (e.g., 10MB per image) via `busboy` or `multer` with disk buffering, never in-memory `Buffer` aggregation.

---

## 4. Regular Expression Denial of Service (ReDoS)

A single catastrophic backtracking regex evaluated against an adversarial payload will freeze an event loop thread at 100% CPU usage for hours.

### Vulnerable Patterns (Catastrophic Backtracking):
- **Nested Quantifiers**: `(a+)+`, `([a-zA-Z]+)*`
- **Overlapping Alternations**: `(a|a)+`, `(a|ab)+`
- **Ambiguous Repetitions**: `^([a-zA-Z0-9_.-]+)+@`

### Defensive Rules:
1. **Never construct regular expressions from user input**.
2. **Refactor nested quantifiers into atomic groups or possessive quantifiers**:
   ```typescript
   // ❌ VULNERABLE: Catastrophic backtracking on 'aaaaaaaaaaaaaaaaaaaaaaaaaaaa!'
   const emailRegex = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;

   // ✅ SAFE: Linear complexity regex
   const safeEmailRegex = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
   ```
3. **Use Linear-Time Engines**: Use Google `re2` (Python `google-re2`, Go native `regexp`) which guarantees $O(N)$ execution time.

---

## 5. Query Pagination & Keyset Pagination Defense

Unbounded `SELECT` queries (`SELECT * FROM logs`) cause OOM server crashes.

### Defensive Rules:
1. **Mandatory Page Size Ceiling**: Clamp client `limit` parameter to a maximum of 100 records:
   ```typescript
   const limit = Math.min(Math.max(parseInt(req.query.limit || "20", 10), 1), 100);
   ```
2. **Keyset / Cursor Pagination over Large `OFFSET`**:
   `OFFSET 500000` requires the database engine to scan 500,000 rows before returning 20. Use cursor pagination:
   ```sql
   -- ✅ Keyset pagination (index seek)
   SELECT id, title, created_at 
   FROM events 
   WHERE created_at < $1 
   ORDER BY created_at DESC 
   LIMIT 20;
   ```
