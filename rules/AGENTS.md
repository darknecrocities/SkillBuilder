# Mandatory Engineering Discipline & Production Etiquette

All software architecture, implementation, refactoring, and pair-programming tasks MUST strictly adhere to the SkillBuilder suite:

1. **Prompt Polishing First (PPE)**:
   - Always analyze, refine, and structure incoming prompts into clear, token-efficient engineering specifications before executing modifications.
2. **Token Savings & High-Density Pairing**:
   - Communicate with high information density. Omit conversational padding. Use targeted diffs and structured markdown tables.
3. **Anti-Mock / Fully Functional Mandate**:
   - Zero static mock arrays pretending to be databases. Wire up real persistence (PostgreSQL, SQLite, structured file stores), real schema validation, and end-to-end integration.
4. **Environment & Secret Hygiene**:
   - Never commit raw credentials. Whenever APIs, databases, or third-party tokens are introduced, maintain `.env.example`, `.env`, and `.gitignore`.
5. **Standardized Containerization**:
   - Provide a production-hardened multi-stage Dockerfile (non-root `USER 10001`, minimal base) and `docker-compose.yml` with health checks.
6. **Network & Request Resilience**:
   - Enforce explicit connection/read timeouts (3s/15s), in-memory caching with invalidation, debouncing on inputs, and bounded exponential backoff with jitter on retries.
7. **Continuous Testing, QA & List-an-Error (LaE)**:
   - Provide automated unit/integration tests for every feature. Whenever an error occurs, catalog its signature, root cause, remediation, and regression test.
8. **Git Branching, Commit Chunking (< 1k lines), & Ready-to-Review PRs**:
   - Branch deliberately (`feat/`, `fix/`), decompose changes into cohesive atomic commits within the 1,000-line budget, and author complete, ready-to-merge Pull Requests.
9. **500-Line Source File Policy**:
   - Maintain a 500-line physical limit on all source files, verified via `scripts/check_source_line_limits.py`.
