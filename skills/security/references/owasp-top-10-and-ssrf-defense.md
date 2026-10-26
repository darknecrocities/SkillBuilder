# OWASP Top 10, SSRF Defense & Secure HTTP Headers

> **Philosophy**: *Never trust outbound destinations or inbound origins. An application that fetches external URLs without post-DNS IP validation will inevitably surrender internal cloud metadata and intranet databases.*

---

## 1. Server-Side Request Forgery (SSRF) Defense

SSRF occurs when a server-side application makes an HTTP request to an untrusted URL supplied by the user (e.g., webhook testing, profile image import, URL previews).

```mermaid
flowchart TD
    A["Untrusted User URL"] --> B["1. Scheme Check (http/https only)"]
    B -->|Passed| C["2. DNS Resolution (A / AAAA records)"]
    B -->|Failed| X["Reject Request"]
    C --> D{"3. IP Range Inspection"}
    D -->|Private RFC 1918 (10.x, 172.16.x, 192.168.x)| X
    D -->|Loopback (127.0.0.1, ::1)| X
    D -->|Link-Local / Metadata (169.254.169.254)| X
    D -->|Multicast / Reserved| X
    D -->|Public Routable IP| E["4. Pin IP & Dispatch HTTP Request"]
```

### 1.1 Invariants for Safe Outbound HTTP Requests:
1. **Strict Scheme Whitelist**: Allow only `http:` and `https:`. Prohibit `file:`, `gopher:`, `dict:`, `ftp:`, `ldap:`.
2. **Post-DNS IP Validation**: Resolve the hostname to an IP address **before** making the connection. Checking hostname strings alone is vulnerable to DNS rebinding and URL parser differentials.
3. **Blacklisted IP Ranges**:
   - `10.0.0.0/8` (RFC 1918 Private)
   - `172.16.0.0/12` (RFC 1918 Private)
   - `192.168.0.0/16` (RFC 1918 Private)
   - `127.0.0.0/8` (IPv4 Loopback)
   - `169.254.0.0/16` (IPv4 Link-Local & AWS/GCP/Azure Metadata `169.254.169.254`)
   - `::1/128` (IPv6 Loopback)
   - `fc00::/7` (IPv6 Unique Local)
   - `fe80::/10` (IPv6 Link-Local)
4. **Pin Socket to Validated IP**: To prevent Time-of-Check to Time-of-Use (TOCTOU) DNS rebinding, connect directly to the validated IP address while passing the original hostname in the `Host` header and TLS SNI.

---

## 2. Content Security Policy (CSP) & Defense-in-Depth Headers

Modern browsers enforce Content Security Policy to eliminate Cross-Site Scripting (XSS), clickjacking, and unauthorized data exfiltration.

### 2.1 Recommended Production Security Headers
```http
Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-{RANDOM_BASE64}' 'strict-dynamic'; object-src 'none'; base-uri 'none'; frame-ancestors 'none';
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

- **`Content-Security-Policy` with Nonce**: Enforces cryptographic nonces on inline scripts, eliminating `'unsafe-inline'`.
- **`X-Content-Type-Options: nosniff`**: Prevents MIME-type sniffing attacks.
- **`Strict-Transport-Security` (HSTS)**: Forces TLS communication for 2 years.

---

## 3. Cross-Origin Resource Sharing (CORS) Security

### Anti-Pattern (Vulnerable):
```typescript
// ❌ VULNERABLE: Wildcard with credentials leaks authenticated sessions
app.use(cors({
  origin: "*",
  credentials: true // Browser will reject or leak sensitive cookies
}));
```

### Defensive Implementation (Explicit Whitelist):
```typescript
import cors from "cors";

const ALLOWED_ORIGINS = new Set([
  "https://app.skillbuilder.io",
  "https://admin.skillbuilder.io"
]);

export const secureCors = cors({
  origin: (origin, callback) => {
    // Allow non-browser requests (tools, curl, server-to-server)
    if (!origin) return callback(null, true);
    
    if (ALLOWED_ORIGINS.has(origin)) {
      return callback(null, true);
    }
    return callback(new Error(`CORS blocked for origin: ${origin}`));
  },
  credentials: true,
  methods: ["GET", "POST", "PUT", "DELETE", "PATCH"],
  allowedHeaders: ["Content-Type", "Authorization", "X-Correlation-ID"]
});
```

---

## 4. Cross-Site Scripting (XSS) & DOM Sanitization

Never inject raw user strings into HTML or inner DOM structures:
```typescript
import DOMPurify from "dompurify";

// ✅ DEFENSIVE: Sanitize before innerHTML
export function renderSafeHtml(container: HTMLElement, rawHtml: string): void {
  const clean = DOMPurify.sanitize(rawHtml, {
    ALLOWED_TAGS: ["b", "i", "em", "strong", "a", "p", "ul", "li", "code", "pre"],
    ALLOWED_ATTR: ["href", "title", "target"]
  });
  container.innerHTML = clean;
}
```
