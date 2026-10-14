# Docker and Containerization Standards

This reference governs container hygiene, security hardening, multi-stage builds, and local orchestration with Docker Compose.

---

## 1. The Containerization Mandate

Every deployable application, backend service, full-stack app, or worker process must provide:
1. A production-hardened **`Dockerfile`**.
2. A matching **`.dockerignore`** file.
3. A **`docker-compose.yml`** orchestrating the service with its dependencies (e.g., PostgreSQL, Redis) and health checks.

---

## 2. Security Hardening Principles

- **Non-Root Execution**: Never run application processes as `root` (UID 0) inside a container. A container breakout with root privileges grants root access on the host node. Always create and switch to an unprivileged user (e.g., `USER appuser` with UID 10001).
- **Multi-Stage Builds**:
  - *Stage 1 (Builder)*: Install full SDKs, compilers (`gcc`, `g++`), development dependencies, and run build/bundling commands.
  - *Stage 2 (Runtime)*: Copy only compiled output and production runtime dependencies into a minimal, stripped base image (`alpine`, `distroless`, or `slim`).
- **Layer Caching Optimization**: Copy dependency manifests (`package.json`, `requirements.txt`, `go.mod`) and install dependencies *before* copying source code. This ensures expensive dependency downloads are cached when only application code changes.
- **Explicit Signal Handling**: Ensure the entrypoint correctly handles `SIGTERM` and `SIGINT` signals for graceful shutdown (e.g., using `tini`, `dumb-init`, or native runtime signal handlers).

---

## 3. Standardized `.dockerignore`

Place this in the repository root alongside the `Dockerfile`:

```dockerignore
# Source control & IDEs
.git
.gitignore
.idea
.vscode
*.swp

# Environment & Local Secrets
.env
.env.*
!.env.example

# Local Dependencies & Virtual Environments
node_modules
vendor
venv
.venv
__pycache__

# Build Outputs & Tests
dist
build
coverage
*.log
.DS_Store

# Docker & CI files
Dockerfile*
docker-compose*.yml
.github
```

---

## 4. Health Checks in Dockerfile and Compose

Containers must explicitly declare how their health is evaluated:

### In Dockerfile
```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1
```

### In Docker Compose
```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD: apppassword
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U appuser -d appdb"]
      interval: 5s
      timeout: 5s
      retries: 5
    volumes:
      - pgdata:/var/lib/postgresql/data

  app:
    build:
      context: .
      dockerfile: Dockerfile
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgres://appuser:apppassword@db:5432/appdb

volumes:
  pgdata:
```
