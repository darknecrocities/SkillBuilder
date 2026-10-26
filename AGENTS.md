# Mandatory Engineering Discipline & Production Etiquette

All software architecture, implementation, refactoring, and pair-programming tasks MUST strictly adhere to the SkillBuilder suite (22 Modular Skills):

1. **Prompt Polishing First (PPE - `/prompt-polish`)**:
   - Analyze, refine, and structure incoming prompts into clear, token-efficient engineering specifications with explicit verification criteria.
2. **Continuous Conversational Learning (CLP - `/continuous-learning`)**:
   - Immediately absorb user corrections and project conventions. Persist invariants to `.agents/learned_conventions.md` via `scripts/record_learning.py` and never repeat corrected mistakes.
3. **Anti-AI-Slop & Clean Craftsmanship (`/anti-slop`)**:
   - Prohibit decorative badges (`shields.io`), synthetic AI marketing copy, obvious restatement comments (`// set loading to true`), and toy mock arrays.
   - Prohibit neon purple gradients, glowing borders, and card-soup layouts.
   - Prohibit raw emojis in interactive UI controls; use semantic Lucide SVG icons with `aria-hidden="true"`.
4. **Autonomous Deep Research & Fallback Pivots (`/research`)**:
   - When any library, package, or build tool fails or is deprecated, autonomously research production alternatives, evaluate trade-offs, and implement drop-in replacements.
5. **Responsiveness QA & Sub-Agent Verification (`/qa`)**:
   - Enforce 4-tier viewport matrix (Mobile 375px, Tablet 768px, Desktop 1280px, Widescreen 1920px+).
   - Zero fixed-pixel containers breaking mobile layouts. Enforce minimum 44x44px touch targets and accessible focus rings.
6. **Anti-Mock / Fully Functional Mandate (`/fullstack`)**:
   - Zero static mock arrays pretending to be databases. Wire up real persistence (PostgreSQL, SQLite, structured file stores), real schema validation, and end-to-end integration.
7. **Token Savings & High-Density Pairing**:
   - Communicate with high information density. Omit conversational padding. Use targeted diffs and structured markdown tables.
8. **Security & Vulnerability Defense (`/security`)**:
   - Never commit raw credentials. Enforce parameterization against SQL/command injection, OWASP Top 10 hardening, and secret hygiene (`.env.example`, `.env`, `.gitignore`).
9. **Standardized Containerization (`/devops`)**:
   - Provide production-hardened multi-stage Dockerfiles (non-root `USER 10001`, minimal base) and `docker-compose.yml` with health checks.
10. **Network & Request Resilience (`/production-etiquette`)**:
    - Enforce explicit connection/read timeouts (3s/15s), in-memory caching with invalidation, debouncing on inputs, and bounded exponential backoff with jitter on retries.
11. **Continuous Testing, QA & List-an-Error (LaE)**:
    - Provide automated unit/integration tests for every feature. Catalog failures with signature, root cause, remediation, and regression test.
12. **Git Branching, Meaningful Commits (Title + Description), Push to Branch & Ready-to-Review PRs (`/git-workflow`, `/full-scale-mode`)**:
    - Branch deliberately (`feat/`, `fix/`, `refactor/`). Enforce the 1,000-line commit budget.
    - Mandatory multi-line commits with Conventional title AND structured description body explaining *Why*, *What*, and *Verification*. Zero lazy commits.
    - Always push commits immediately to the remote branch (`git push origin <branch>`).
    - Always author or update an active, ready-to-merge GitHub Pull Request with complete context, verification evidence, and rollback plans.
13. **Multi-Tiered Code Quality, 500-Line Limit & Full-Scale Orchestration (`/full-scale-mode`, `/world-class-engineering`, `/refactor`)**:
    - Maintain a strict 500-line physical ceiling on all source files, verified via `check_source_line_limits.py --show-tiers`.
    - Proactively decompose modules entering the 350-line warning zone into cohesive domain slices (target sweet spot: 150–250 lines).
    - Enforce cognitive hygiene: maximum 40 physical lines per function, maximum 3 nesting levels with early return guard clauses, and cyclomatic complexity $\le 10$. Zero arbitrary file-shredding.
