# Mandatory Engineering Discipline & Production Etiquette

For all software engineering, architecture, development, bug fixing, and refactoring tasks across all projects:

1. **Mandatory Skill Compliance**:
   - You MUST automatically activate and adhere strictly to the `world-class-engineering` and `production-etiquette` skills.
   - Do NOT treat them as optional. Execute the 6-phase Engineering Operating System (EOS: Understand -> Define -> Plan -> Implement -> Verify -> Deliver).

2. **Secrets & Environment Hygiene**:
   - Whenever APIs, databases, authentication, or external services are touched or created, immediately verify and configure `.env.example`, `.env`, and `.gitignore`.
   - Never commit raw credentials.

3. **Standardized Containerization**:
   - Provide a production-hardened multi-stage Dockerfile (non-root user, minimal base) and `docker-compose.yml` with health checks.

4. **Deep Pre-Planning Research**:
   - Inspect the real codebase, dependencies, lockfiles, and official documentation before authoring any implementation plan.
   - Do not guess or hallucinate API signatures or CLI flags.

5. **Network & Request Resilience**:
   - Enforce explicit connection/read timeouts (default 3s/15s), in-memory caching with invalidation, debouncing on inputs, and bounded exponential backoff with jitter on retries.

6. **Anti-Mock / Fully Functional Mandate**:
   - Strictly avoid static mock arrays or toy interactive demos; all features must have real persistence, validation schemas, and complete error handling.

7. **Continuous Testing & CI/CD**:
   - Provide automated unit/integration tests for every feature and maintain an automated CI/CD pipeline (`.github/workflows/ci.yml`).

8. **Git Branching, Commit Chunking (< 1k lines), & Ready-to-Review PRs**:
   - Branch deliberately (`feat/`, `fix/`, `refactor/`), decompose changes into cohesive atomic commits within the 1,000-line budget, and author complete, ready-to-merge Pull Requests.

9. **500-Line Source File Policy**:
   - Maintain a 500-line physical limit on all source files, verified via `check_source_line_limits.py`.
