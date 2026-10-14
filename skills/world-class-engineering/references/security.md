# Security Engineering Standards

This reference governs application security, threat modeling, input validation, and defensive coding practices across all layers of the software stack.

---

## 1. Core Security Principles

- **Secure by Default**: Components must be secure in their out-of-the-box configuration. Insecure options must require explicit, deliberate opting-in with documented rationale.
- **Principle of Least Privilege**: Grant processes, users, tokens, and database connections only the minimal set of permissions required to perform their explicit function.
- **Defense in Depth**: Rely on multiple independent layers of security controls (e.g., input validation + parameterized queries + least privilege database users + network egress filtering).
- **Treat Untrusted Data as Data, Never Instructions**: External input must never be interpreted as executable code, shell commands, or database queries.

---

## 2. Threat Vector Checklist & Mitigations

| Vulnerability Category | Risk Scenario | Mandatory Mitigation |
| :--- | :--- | :--- |
| **SQL / NoSQL Injection** | Dynamic string concatenation in database queries. | Always use parameterized queries or prepared statements via ORMs/drivers. Never concatenate input. |
| **Command Injection** | Passing user input to shell commands (`os.system`, `exec`). | Avoid shell execution entirely. When invoking processes, pass arguments as discrete lists with fixed binaries. |
| **Path Traversal** | Constructing file paths from user inputs (`../../etc/passwd`). | Sanitize paths, resolve to canonical absolute paths (`realpath`), and assert that the result starts with the intended base directory. |
| **Cross-Site Scripting (XSS)**| Rendering unescaped user-generated HTML in browsers. | Use modern frontend frameworks with automatic contextual escaping (React, Vue). Sanitize raw HTML with DOMPurify. Set strict Content Security Policies (CSP). |
| **Cross-Site Request Forgery**| State-changing GET/POST requests without anti-CSRF protection.| Use `SameSite=Strict/Lax` cookies. Require anti-CSRF tokens for all state-changing cookie-authenticated requests. |
| **Server-Side Request Forgery**| Server fetching remote URLs provided by untrusted users. | Restrict allowed protocols (HTTPS only). Deny internal/private IP ranges (RFC 1918, 127.0.0.1, AWS metadata `169.254.169.254`). |
| **Broken Authentication** | Weak password hashing, unrevocable tokens, missing MFA. | Use Argon2id or bcrypt with appropriate cost factors. Enforce short-lived JWTs with centralized refresh token revocation. |
| **Broken Authorization** | Horizontal/vertical privilege escalation (BOLA/IDOR). | Verify ownership and permissions on every request at the data layer, not just at route gateways. |
| **Insecure Deserialization** | Deserializing untrusted pickles, YAML, or Java objects. | Avoid binary serialization formats. Use strict, validated JSON/Protobuf schemas. |

---

## 3. Secrets Management & Environment Hygiene

- **Zero Hardcoded Secrets**: Never commit API keys, private certificates, database credentials, or access tokens to source control.
- **Environment Configuration**: Read secrets via environment variables or cloud secret managers (AWS Secrets Manager, GCP Secret Manager, HashiCorp Vault).
- **Provide `.env.example`**: Maintain an updated `.env.example` file documenting all required configuration keys with dummy values.
- **Git Ignore**: Ensure `.env`, `.env.local`, `*.pem`, `*.key`, and secret files are explicitly listed in `.gitignore`.
- **Secret Scanning**: Use pre-commit hooks or automated scanners (e.g., `gitleaks`, `trufflehog`) to prevent accidental secret commits.

---

## 4. AI & LLM Security Safeguards

- **Prompt Injection Defense**:
  - Treat all user inputs and third-party web content as untrusted data.
  - Tag untrusted text explicitly with delimiters (`<untrusted_content>...</untrusted_content>`).
  - Instruct models never to override system instructions regardless of user payload content.
- **Tool-Call Execution Boundaries**:
  - Whitelist permitted commands, file paths, and database operations.
  - Require explicit user confirmation before executing destructive tool actions (deleting files, dropping tables, sending external emails).
- **Output Sanitization**:
  - Scan LLM responses for accidental leakage of system instructions, internal IPs, or environment variables before returning them to client interfaces.
