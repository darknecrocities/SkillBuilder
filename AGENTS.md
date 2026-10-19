# Mandatory Engineering Discipline & Production Etiquette

All software architecture, implementation, refactoring, and pair-programming tasks MUST strictly adhere to the SkillBuilder suite:

1. **Prompt Polishing First (PPE)**:
   - Always analyze, refine, and structure incoming prompts into clear, token-efficient engineering specifications before executing modifications.
2. **Continuous Conversational Learning (CLP)**:
   - Immediately absorb user corrections and project conventions. Persist invariants to `.agents/learned_conventions.md` via `scripts/record_learning.py` and never repeat corrected mistakes.
3. **Anti-Vibe-Coding UI Standards**:
   - Strictly prohibit neon purple gradients, glowing green borders, card-soup layouts, decorative badges, and synthetic AI marketing copywriting.
   - Strictly prohibit raw emojis in UI buttons, headings, and navigation. Use semantic SVG vector icons (Lucide Icons) with accessible attributes.
4. **Token Savings & High-Density Pairing**:
   - Communicate with high information density. Omit conversational padding. Use targeted diffs and structured markdown tables.
5. **Anti-Mock / Fully Functional Mandate**:
   - Zero static mock arrays pretending to be databases. Wire up real persistence (PostgreSQL, SQLite, structured file stores), real schema validation, and end-to-end integration.
6. **Environment & Secret Hygiene**:
   - Never commit raw credentials. Whenever APIs, databases, or third-party tokens are introduced, maintain `.env.example`, `.env`, and `.gitignore`.
7. **Standardized Containerization**:
   - Provide a production-hardened multi-stage Dockerfile (non-root `USER 10001`, minimal base) and `docker-compose.yml` with health checks.
8. **Network & Request Resilience**:
   - Enforce explicit connection/read timeouts (3s/15s), in-memory caching with invalidation, debouncing on inputs, and bounded exponential backoff with jitter on retries.
9. **Continuous Testing, QA & List-an-Error (LaE)**:
   - Provide automated unit/integration tests for every feature. Whenever an error occurs, catalog its signature, root cause, remediation, and regression test.
10. **Git Branching, Commit Chunking (< 1k lines), & Ready-to-Review PRs**:
   - Branch deliberately (`feat/`, `fix/`), decompose changes into cohesive atomic commits within the 1,000-line budget, and author complete, ready-to-merge Pull Requests.
11. **500-Line Source File Policy**:
   - Maintain a 500-line physical limit on all source files, verified via `scripts/check_source_line_limits.py`.
