# Mandatory Engineering Discipline & Production Etiquette

All software architecture, implementation, refactoring, and development tasks in this repository MUST strictly adhere to both the `world-class-engineering` and `production-etiquette` skills:

1. **Environment & Secret Hygiene**:
   - Whenever APIs, databases, or third-party tokens are introduced, automatically verify and configure `.env.example`, `.env`, and `.gitignore`.
2. **Standardized Containerization**:
   - Provide a production-hardened multi-stage Dockerfile (non-root user, minimal base) and `docker-compose.yml` with health checks.
3. **Deep Pre-Planning Research**:
   - Perform empirical codebase and official documentation research before formulating any plan.
4. **Network & Request Resilience**:
   - Enforce explicit connection/read timeouts, in-memory caching with invalidation, debouncing on inputs, and bounded exponential backoff with jitter on retries.
5. **Anti-Mock / Fully Functional Mandate**:
   - Strictly avoid static mock arrays or toy interactive demos; all features must have real persistence, validation schemas, and complete error handling.
6. **Continuous Testing & CI/CD**:
   - Provide automated unit/integration tests for every feature and maintain an automated CI/CD pipeline (`.github/workflows/ci.yml`).
7. **Git Branching, Commit Chunking (< 1k lines), & Ready-to-Review PRs**:
   - Branch deliberately (`feat/`, `fix/`), decompose changes into cohesive atomic commits within the 1,000-line budget, and author complete, ready-to-merge Pull Requests.
8. **500-Line Source File Policy**:
   - Maintain a 500-line physical limit on all source files, verified via `scripts/check_source_line_limits.py`.
