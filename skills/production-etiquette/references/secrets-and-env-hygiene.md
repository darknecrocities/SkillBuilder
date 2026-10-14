# Secrets and Environment Hygiene Standards

This reference governs environment variable management, secret protection, `.gitignore` maintenance, and boot-time configuration validation.

---

## 1. The Automatic Trigger Rule

Whenever an implementation introduces:
- A third-party API client (Stripe, OpenAI, Twilio, SendGrid, GitHub API, etc.).
- A database connection string (`DATABASE_URL`, `POSTGRES_PASSWORD`).
- Authentication secrets (`JWT_SECRET`, `SESSION_SECRET`, `COOKIE_KEY`).
- External service URLs or ports (`PORT`, `REDIS_URL`).

You **MUST** immediately verify and establish two foundational hygiene files before committing code:
1. **`.gitignore`**: Guarantees that secrets and local files can never be committed.
2. **`.env.example`**: Documents all configuration requirements for other engineers and CI/CD pipelines.

---

## 2. Standardized `.gitignore` Specification

Every project repository must contain a comprehensive `.gitignore` covering:

```gitignore
# Environment & Secrets (NEVER COMMIT)
.env
.env.*
!.env.example
*.key
*.pem
*.cert
*.crt
id_rsa
secrets/

# Dependencies
node_modules/
vendor/
venv/
.venv/
__pycache__/
*.pyc

# Build & Distribution Artifacts
dist/
build/
out/
.next/
.nuxt/
target/
*.egg-info/

# Logs & Diagnostics
*.log
npm-debug.log*
yarn-debug.log*
coverage/
.nyc_output/

# Operating System & IDE Files
.DS_Store
Thumbs.db
.idea/
.vscode/
*.swp
*.swo
```

---

## 3. Standardized `.env.example` Specification

The `.env.example` file serves as the explicit, living configuration contract. Follow these rules:

1. **Document Every Key**: Every environment variable read in the codebase must appear in `.env.example`.
2. **Safe Defaults & Descriptive Placeholders**: Use clear dummy values indicating the expected format:
   ```bash
   # Server Configuration
   PORT=3000
   NODE_ENV=development
   LOG_LEVEL=info

   # Database Connection (PostgreSQL)
   DATABASE_URL=postgres://appuser:apppassword@localhost:5432/appdb

   # Authentication & Security
   # Generate a 32-character random string: openssl rand -base64 32
   JWT_SECRET=your_jwt_secret_min_32_characters_here
   JWT_EXPIRES_IN=15m
   REFRESH_TOKEN_EXPIRES_IN=7d

   # Third-Party Integrations
   STRIPE_API_KEY=sk_test_placeholder_key_here
   STRIPE_WEBHOOK_SECRET=whsec_placeholder_secret_here
   ```
3. **Never Include Production Credentials**: `.env.example` is committed to Git; it must never contain live production keys.

---

## 4. Boot-Time Configuration Validation (Fail-Fast)

Never access `process.env.VAR` or `os.environ.get("VAR")` scattered across the codebase without validation. Validate and freeze configuration at startup:

### TypeScript (Zod Example)
```typescript
import { z } from "zod";

const envSchema = z.object({
  PORT: z.coerce.number().default(3000),
  NODE_ENV: z.enum(["development", "production", "test"]).default("development"),
  DATABASE_URL: z.string().url("DATABASE_URL must be a valid connection string"),
  JWT_SECRET: z.string().min(32, "JWT_SECRET must be at least 32 characters"),
});

export const env = envSchema.parse(process.env);
```

### Python (Pydantic Settings Example)
```python
from pydantic_settings import BaseSettings
from pydantic import Field, PostgresDsn

class AppConfig(BaseSettings):
    port: int = Field(default=8000)
    database_url: PostgresDsn
    jwt_secret: str = Field(min_length=32)

    class Config:
        env_file = ".env"
        extra = "ignore"

config = AppConfig()
```

If any mandatory variable is missing or malformed, the process immediately crashes with a descriptive message before opening sockets or accepting requests.
