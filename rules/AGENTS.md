# Mandatory Engineering Discipline & Production Etiquette

All software architecture, implementation, refactoring, and pair-programming tasks MUST strictly adhere to the SkillBuilder suite (35 Modular Skills):

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
5. **Responsiveness QA & Platform Domain Specialization (`/qa`, `/mobile-ui`, `/web-ui`)**:
   - Enforce 4-tier viewport matrix (Mobile 375px, Tablet 768px, Desktop 1280px, Widescreen 1920px+).
   - Zero fixed-pixel containers breaking mobile layouts. Enforce minimum 44x44px touch targets and accessible focus rings.
   - Enforce Platform Domain Specialization (PDS): Mount `/mobile-ui` for mobile targets and `/web-ui` for web targets. Never inject cross-platform styling bloat.
6. **Anti-Mock / Fully Functional Mandate (`/fullstack`)**:
   - Zero static mock arrays pretending to be databases. Wire up real persistence (PostgreSQL, SQLite, structured file stores), real schema validation, content-hashed pre-mutation backups, and end-to-end integration.
7. **Token Savings & Quota Preservation (`/full-scale-mode`, `/prompt-polish`)**:
   - Communicate with high information density. Omit conversational padding. Use targeted diffs and structured markdown tables.
   - Dynamically prune inapplicable domain skills in Phase 1 to eliminate context rot and save ~1,850 tokens per turn.
8. **Security & Vulnerability Defense (`/security`)**:
   - Never commit raw credentials. Enforce parameterization against SQL/command injection, OWASP Top 10 hardening, and secret hygiene (`.env.example`, `.env`, `.gitignore`).
   - Zero silent error swallowing (`catch (e) {}` / `except: pass`). Sanitize unhandled exceptions into RFC 7807 Problem Details with correlation IDs (`X-Correlation-ID`) and zero production stack leaks.
   - Enforce refresh token family rotation with reuse detection, constant-time comparison (`crypto.timingSafeEqual`, `hmac.compare_digest`), and strict cookie flags (`Secure; HttpOnly; SameSite=Lax`).
   - Guard against application-layer DDoS: sliding-window/token-bucket rate limits, Slowloris timeouts (3s handshake / 15s body), 100KB payload caps, and ReDoS catastrophic backtracking prevention.
   - Validate outbound URLs post-DNS (SSRF defense), strictly blocking RFC 1918 private subnets and cloud metadata (`169.254.169.254`). Enforce tenant-scoped database queries (`WHERE id = $1 AND tenant_id = $2`) against BOLA/IDOR.
9. **Standardized Containerization & Cloud Deployment (`/devops`, `/gcp`, `/aws`, `/firebase`, `/supabase`)**:
   - Provide production-hardened multi-stage Dockerfiles (non-root `USER 10001`, minimal base) and `docker-compose.yml` with health checks.
   - Enforce cloud least privilege, Secret Manager bindings, Row-Level Security (RLS) on serverless stores, and stateful deletion protection (`RemovalPolicy.RETAIN`, `deletion_protection = true`).
10. **Network & Request Resilience (`/production-etiquette`)**:
    - Enforce explicit connection/read timeouts (3s/15s), in-memory caching with invalidation, debouncing on inputs, and bounded exponential backoff with jitter on retries.
11. **Continuous Testing, QA & List-an-Error (LaE) (`/testing`, `/qa`)**:
    - Provide automated unit/integration tests for every feature. Use semantic ARIA queries over XPath/testId soup. Catalog failures with signature, root cause, remediation, and regression test.
12. **Git Branching, Meaningful Commits (Title + Description), Push to Branch & Ready-to-Review PRs (`/git-workflow`, `/full-scale-mode`)**:
    - Branch deliberately (`feat/`, `fix/`, `refactor/`). Enforce the 1,000-line commit budget.
    - Mandatory multi-line commits with Conventional title AND structured description body explaining *Why*, *What*, and *Verification*. Zero lazy commits.
    - Always push commits immediately to the remote branch (`git push origin <branch>`).
    - Always author or update an active, ready-to-merge GitHub Pull Request with complete context, verification evidence, and rollback plans.
13. **Multi-Tiered Code Quality, 500-Line Limit & Modular Architecture (`/world-class-engineering`, `/refactor`, `/routing`, `/state-management`)**:
    - Maintain a strict 500-line physical ceiling on all source files, verified via `check_source_line_limits.py --show-tiers`.
    - Proactively decompose modules entering the 350-line warning zone into cohesive domain slices (target sweet spot: 150–250 lines).
    - Enforce cognitive hygiene: maximum 40 physical lines per function, maximum 3 nesting levels with early return guard clauses, and cyclomatic complexity $\le 10$. Zero arbitrary file-shredding.
14. **3-Phase Triad Cadence & Autonomous Skill Resonance (`/full-scale-mode`)**:
    - Orchestrate complex deliverables through the 3-Phase Triad Cadence (Phase 1: Frontend & Interface Architecture -> Phase 2: Backend, Cloud & Data Infrastructure -> Phase 3: Testing, QA & Verifiable Release).
    - Leverage Autonomous Skill Resonance (ASR) to detect project fingerprints and automatically bind relevant domain skills.
15. **Autonomous Project Skill Minting (`/project-skills`)**:
    - When establishing unique, project-specific architectures, agents mint self-contained project skills under `.agents/skills/<skill-name>/SKILL.md` using the Skill Synthesis Protocol (SSP).
16. **Deduplicated Storage Backups, Sensitive Deletion Disclosure & Multi-Agent Synchronization (`/database`, `/firebase`, `/supabase`, `/gcp`, `/aws`, `/full-scale-mode`)**:
    - **Idempotent Single-Slot Backups (Zero Spam)**: Before schema migrations, bulk writes, or storage rule changes, verify or create a single canonical backup keyed by SHA-256 content/schema digest in `.backups/backup_manifest.json` (`manage_deduplicated_backup.py`). Never generate redundant timestamped copies (`*.bak.1`, `*.bak.2`, `dump_copy.sql`) when state is unchanged or across concurrent agent turns.
    - **Sensitive Deletion Human-in-the-Loop Gate**: Always halt and warn the user first before executing any destructive deletion (`DROP TABLE/COLUMN`, `TRUNCATE`, unconditioned `DELETE`, Firestore/Supabase collection or bucket removal, `RemovalPolicy.DESTROY`, `force_destroy = true`, or sensitive file deletion). Disclose the target resource, sensitivity tier, affected scope, and verified backup SHA-256 hash, and await explicit user confirmation.
    - **Simultaneous Multi-Agent Synchronization**: Concurrent subagents working simultaneously must respect partitioned file ownership, coordinate storage mutations through the shared `.backups/backup_manifest.json` lease lock, and keep all 35 skills and multi-platform instruction files 100% synchronized.
