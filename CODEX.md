# CODEX.md - OpenAI & ChatGPT System Instructions

> Production Engineering Standards for OpenAI Codex, GPT-4o, and ChatGPT.

# Mandatory Engineering Discipline & Production Etiquette

All software architecture, implementation, refactoring, and pair-programming tasks MUST strictly adhere to the SkillBuilder suite (36 Modular Skills):

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
14. **Structured 5-Stage Lifecycle, Orchestration Memory & Harness Engineering (`/full-scale-mode`, `/world-class-engineering`)**:
    - Orchestrate complex deliverables through the 5-Stage Delivery Lifecycle (Stage 1: Discover & Memory Recall -> Stage 2: Plan & Architectural Blueprint -> Stage 3: Build & Atomic Execution -> Stage 4: Verify & Harness Loop -> Stage 5: Release & Memory Consolidation).
    - Maintain structured active session memory in `.agents/memory/orchestration_state.json` via `manage_orchestration_memory.py` across multi-turn handoffs.
    - Enforce the 5-Tier Evaluation Harness (`orchestration_harness.py`) and bounded Autonomous Self-Healing Loop (maximum 3 iterations) before authorizing any release.
    - Leverage Autonomous Skill Resonance (ASR) and Platform Domain Specialization (PDS) to prune cross-platform context bloat.
15. **Autonomous Project Skill Minting (`/project-skills`)**:
    - When establishing unique, project-specific architectures, agents mint self-contained project skills under `.agents/skills/<skill-name>/SKILL.md` using the Skill Synthesis Protocol (SSP).
16. **Deduplicated Storage Backups, Sensitive Deletion Disclosure & Multi-Agent Synchronization (`/database`, `/firebase`, `/supabase`, `/gcp`, `/aws`, `/full-scale-mode`)**:
    - **Idempotent Single-Slot Backups (Zero Spam)**: Before schema migrations, bulk writes, or storage rule changes, verify or create a single canonical backup keyed by SHA-256 content/schema digest in `.backups/backup_manifest.json` (`manage_deduplicated_backup.py`). Never generate redundant timestamped copies (`*.bak.1`, `*.bak.2`, `dump_copy.sql`) when state is unchanged or across concurrent agent turns.
    - **Sensitive Deletion Human-in-the-Loop Gate**: Always halt and warn the user first before executing any destructive deletion (`DROP TABLE/COLUMN`, `TRUNCATE`, unconditioned `DELETE`, Firestore/Supabase collection or bucket removal, `RemovalPolicy.DESTROY`, `force_destroy = true`, or sensitive file deletion). Disclose the target resource, sensitivity tier, affected scope, and verified backup SHA-256 hash, and await explicit user confirmation.
    - **Simultaneous Multi-Agent Synchronization**: Concurrent subagents working simultaneously must respect partitioned file ownership, coordinate storage mutations through the shared `.backups/backup_manifest.json` lease lock, and keep all 36 skills and multi-platform instruction files 100% synchronized.
17. **Antigravity Automation & Background Execution (`/antigravity-automation`, `/full-scale-mode`)**:
    - **Scheduled Sidecars**: Structure background scheduled automations in `~/.gemini/jetski/sidecars/<slug>/sidecar.json` with strict timezone awareness (`CRON_TZ`) and self-contained execution prompts.
    - **In-Session Scheduling & Zero Polling**: Standardize in-turn timers (`DurationSeconds`, `TimerCondition`) and recurring jobs via the native `schedule` tool. Never poll in loops or use shell `sleep`.
    - **Active Lifecycle Hooks**: Enforce plugin-level safety gates (`PreToolUse`, `PostToolUse`, `SessionStart`) via `hooks.json` to prevent destructive deletions and enforce the 500-line source ceiling.


## Skill Index (37 Skills)
- `/3d`: Interactive 3D WebGL, Three.js, and React Three Fiber (R3F) engineering skill. Enforces 60fps budgets, PBR materials, Draco compression, and studio lighting.
- `/ai`: Architect, implement, and maintain production AI systems, Gemini API agents, Antigravity multi-agent orchestration, structured JSON outputs, reliable tool calling, and RAG retrieval pipelines.
- `/anti-slop`: Anti-AI-slop and clean craftsmanship skill. Eliminates decorative badges, fake mock databases, neon gradients, obvious comments, and marketing fluff.
- `/antigravity-automation`: Automate recurring, background, event-driven, and multi-agent workflows in Google Antigravity. Crafts scheduled sidecars (~/.gemini/jetski/sidecars/<slug>/sidecar.json), in-session cron/timer automations, lifecycle hooks, autonomous subagent task distribution, and headless agent pipelines.
- `/api-design`: API contract design and OpenAPI 3.1 specification skill. Enforces RFC 7807 problem details, idempotency headers, and consistent status codes.
- `/aws`: Amazon Web Services resilient cloud architecture, serverless Lambda execution, S3 bucket security, DynamoDB single-table design, and IAM least privilege.
- `/backend`: Architect, implement, and maintain resilient backend services, clean architecture, REST/gRPC API contracts, strict schema validation, authentication, rate-limiting, and error handling.
- `/continuous-learning`: Continuous conversational learning protocol (CLP) skill. Persists user corrections and project conventions to .agents/learned_conventions.md to prevent repeating mistakes.
- `/data-pipelines`: Data pipeline engineering, streaming ETL with backpressure, Apache Arrow memory structures, DuckDB in-process analytics, schema validation, and dead-letter queues (DLQ).
- `/database`: Architect, implement, and maintain resilient relational and NoSQL databases, zero-downtime schema migrations (expand/contract), index optimization, and connection pooling.
- `/devops`: Architect, implement, and maintain secure cloud infrastructure on GCP/AWS, multi-stage non-root Docker containers, Terraform IaC, CI/CD pipelines, and OpenTelemetry observability.
- `/firebase`: Firebase serverless architecture, Cloud Firestore schema design, Security Rules (firestore.rules, storage.rules), Firebase Auth, and Admin SDK.
- `/frontend`: Frontend architecture, state management, and lifecycle engineering skill. Governs React 19, Next.js, and Flutter with clean boundary isolation.
- `/full-scale-mode`: Master Project Orchestration Engine (aliased as /world-class-engineering). Unifies all 36 SkillBuilder skills across the 5-Stage Lifecycle (Discover, Plan, Build, Harness Loop, Release), Orchestration Memory (.agents/memory/), and the 3-Phase Triad Cadence.
- `/fullstack`: Fullstack rapid delivery skill with the strict anti-mock mandate. Builds complete vertical slices with real persistence, validation, and zero toy data.
- `/gcp`: Google Cloud Platform architecture, Cloud Run serverless deployment, Pub/Sub, Secret Manager, Cloud SQL, and IAM least-privilege security.
- `/git-workflow`: Git branching, atomic commit chunking, and release management skill. Enforces the 1,000-line commit budget, Conventional Commits, and PR authoring.
- `/i18n`: Multi-locale internationalization architecture, ICU MessageFormat, RTL bidirectional layout mirroring, and cultural localization.
- `/local-llm`: Local LLM architecture, quantized inference (GGUF Q4_K_M/Q8_0), Ollama, llama.cpp, Apple Silicon MLX, WebLLM, GBNF structured grammars, in-process local RAG, and 3-tier hybrid edge-cloud routing.
- `/mobile-ui`: Native mobile UI/UX craftsmanship, kinetic motion, and tactile engineering skill for iOS (SwiftUI/HIG 18/19), Android (Material 3 Expressive/Jetpack Compose), React Native, and Flutter.
- `/observability`: Observability and telemetry engineering skill. Enforces OpenTelemetry distributed tracing, structured JSON logging with correlation IDs, and health probes.
- `/performance`: Performance profiling and optimization skill. Audits Core Web Vitals (LCP, CLS, INP), N+1 queries, bundle budgets, and memory leaks.
- `/production-etiquette`: >-
- `/project-skills`: Autonomous Project Skill Synthesis Protocol (SSP). Introspects repository dependencies, conventions, and architecture to mint persistent, tailored domain skills in .agents/skills/<project-skill>/SKILL.md.
- `/prompt-polish`: Evaluates, manages, and polishes user prompts into token-efficient, crystal-clear engineering specifications with explicit constraints, verification criteria, and edge-case coverage before code generation.
- `/qa`: Comprehensive Two-Tier Quality Assurance skill. Features Full UI/Frontend QA (viewports, touch ergonomics, WCAG 2.2 AA, sub-pixel lighting, 120Hz compositor) and Full App Functional QA (state machines, real persistence, 3s/15s network resilience, mobile OS lifecycle, memory leaks, security, and Master Error Catalog).
- `/refactor`: Safe refactoring and technical debt remediation skill. Enforces Strangler Fig patterns, characterization testing, and decomposition of bloated files.
- `/research`: Autonomous deep researcher and fallback engine. Evaluates trade-offs and discovers production-grade alternatives when dependencies fail or libraries are deprecated.
- `/routing`: Modern file-based routing architecture, Next.js App Router, layout hierarchies, parallel/intercepting routes, and Flutter declarative navigation.
- `/security`: Security hardening and vulnerability defense skill. Enforces OWASP Top 10 mitigations, zero hardcoded secrets, input sanitization, and SQL parameterization.
- `/state-management`: Declarative state machines, TanStack Query server-state caching, invalidation, optimistic updates, atomic Zustand slices, and signals.
- `/supabase`: Supabase fullstack architecture, PostgreSQL Row Level Security (RLS), Supabase Auth, Edge Functions, and pgvector embeddings.
- `/testing`: Test-Driven Development (TDD) discipline, Vitest, Jest, Playwright E2E with accessible locators, MSW contract tests, and mutation testing principles.
- `/ui`: UI design systems, tokens, Apple HIG, and glassmorphism craftsmanship skill. Enforces disciplined neutral palettes, fluid typography, Cupertino materials, and semantic Lucide SVG icons.
- `/video-editing`: Production motion graphics, video editing, programmatic animation, and audio-visual synchronization. Embodies the 17 Awesome Claude motion styles (Swiss kinetic type, liquid morphing, HUD drafting, live line drawing, 3D card flips), high-performance Python-to-FFmpeg rawvideo pipelines, tempo-locked BPM grid choreography, and broadcast audio mastering.
- `/web-ui`: Modern web design systems, Component-Level Container Queries (@container), CSS View Transitions API, OKLCH perceptual color spaces, fluid clamp() typography curves, and single-zenith sub-pixel lighting craftsmanship.
- `/world-class-engineering`: A rigorous engineering skill for architecture, implementation, refactoring, AI/ML integration, testing, security, code review, and production-quality software delivery.

## Developer Directives
1. Multi-tiered maintainability: strict 500-line ceiling, 350-line warning threshold, and 150–250 line sweet spot.
2. Never interpolate variables into SQL queries (prevent SQL injection).
3. Zero decorative badges, shields.io icons, or synthetic AI marketing copy.
4. Autonomous research: when a library is broken, evaluate and recommend drop-in replacements.
5. Idempotent Single-Slot Backups: maintain a single SHA-256 content-hashed backup per resource state; never spam duplicate backup files across concurrent agent runs.
6. Sensitive Deletion Gate: always notify the user with impact scope and backup hash before deleting tables, columns, buckets, collections, or sensitive files.
