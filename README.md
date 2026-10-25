```text
  ███████╗██╗  ██╗██╗██╗     ██╗     ██████╗ ██╗   ██╗██╗██╗     ██████╗ ███████╗██████╗ 
  ██╔════╝██║ ██╔╝██║██║     ██║     ██╔══██╗██║   ██║██║██║     ██╔══██╗██╔════╝██╔══██╗
  ███████╗█████═╝ ██║██║     ██║     ██████╔╝██║   ██║██║██║     ██║  ██║█████╗  ██████╔╝
  ╚════██║██╔═██╗ ██║██║     ██║     ██╔══██╗██║   ██║██║██║     ██║  ██║██╔══╝  ██╔══██╗
  ███████║██║ ╚██╗██║███████╗███████╗██████╔╝╚██████╔╝██║███████╗██████╔╝███████╗██║  ██║
  ╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═════╝  ╚═════╝ ╚═╝╚══════╝╚═════╝ ╚══════╝╚═╝  ╚═╝
```

# SkillBuilder: Anti-AI-Slop Dynamic Engineering Ecosystem

SkillBuilder is a production-grade suite of **20 specialized Agent Skills** and architectural guardrails designed for **Google Antigravity**. Authored by **Arron Kian Parejas (@darknecrocities)**, it eliminates generic AI slop, decorative badges, toy mock databases, and overengineered buzzwords—transforming AI coding agents into disciplined senior software architects and pair programmers.

---

## Operating Philosophy

Most AI code generation defaults to synthetic tropes: bloated comments explaining obvious lines, fake in-memory mock arrays pretending to be databases, neon purple gradients with glowing borders, and unmaintained dependency choices that fail in production.

SkillBuilder enforces an uncompromising engineering standard:

> **Understand first. Polish the prompt. Learn continuously. Eliminate AI slop. Build real persistence. Test viewports relentlessly. Catalog errors. Deliver production software.**

---

## Table of Contents

1. [The 20 Modular Skills (`/`)](#the-20-modular-skills-)
2. [Anti-AI-Slop & Craftsmanship](#anti-ai-slop--craftsmanship)
3. [Autonomous Research & Fallback Pivots](#autonomous-research--fallback-pivots)
4. [Responsiveness QA & Sub-Agent Verification](#responsiveness-qa--sub-agent-verification)
5. [Developer Workspace (`workspace/`)](#developer-workspace-workspace)
6. [Continuous Conversational Learning (CLP)](#continuous-conversational-learning-clp)
7. [Installation & Antigravity Integration](#installation--antigravity-integration)
8. [Automated Verification Suites (25 Suites)](#automated-verification-suites-25-suites)
9. [Repository Architecture](#repository-architecture)

---

## The 20 Modular Skills (`/`)

Every skill is directly discoverable and executable via `/` slash commands in Antigravity:

| Slash Command | Skill Name | Core Architectural Responsibility |
| :--- | :--- | :--- |
| `/world-class-engineering` | **World-Class Engineering** | Master EOS orchestrator (Understand -> Define -> Plan -> Implement -> Verify -> Deliver), 500-line source file policy. |
| `/anti-slop` | **Anti-AI-Slop Sanitizer** | Purges decorative badges (`shields.io`), marketing copy, obvious comments, and fake mock databases. |
| `/research` | **Autonomous Research & Fallbacks** | Discovers modern, production-grade library alternatives when dependencies fail or are deprecated. |
| `/qa` | **Responsiveness QA & Sub-Agents** | Viewport testing (375px/768px/1280px+), a11y (WCAG AA), touch targets (>=44px), Master Error Catalog. |
| `/ui` | **UI Design Systems & Tokens** | High-contrast neutral scales (zinc/slate), fluid typography, Lucide SVG vector icons (no raw emojis). |
| `/frontend` | **Frontend Architecture** | Pure UI separation, React 19, Next.js App Router, Flutter, `useEffect` AbortController cleanup. |
| `/backend` | **Backend Systems Engineering** | Clean architecture (Hexagonal), domain boundaries, strict runtime validation (Zod, Pydantic v2). |
| `/security` | **Security Hardening** | OWASP Top 10 defenses, zero hardcoded secrets, SQL injection defense, CORS/CSP policies. |
| `/fullstack` | **Fullstack Anti-Mock Delivery** | Complete vertical slices from UI to database (PostgreSQL/SQLite) with zero fake mock arrays. |
| `/database` | **Database & Datastores** | Zero-downtime migrations (expand/contract), index optimization, ACID transactional integrity. |
| `/devops` | **Cloud & Container DevOps** | Hardened multi-stage Dockerfiles (`USER 10001`), docker-compose, CI/CD pipelines, distroless images. |
| `/ai` | **AI & LLM Engineering** | Production Gemini SDK, structured JSON outputs (`response_schema`), defensive tool calling, token budgets. |
| `/prompt-polish` | **Prompt Refinement (PPE)** | 5-phase Prompt Polishing Engine transforming raw requests into token-efficient specifications. |
| `/production-etiquette` | **Production Etiquette** | Secret hygiene (`.env.example`), resilient network client (timeouts 3s/15s, retry with jitter). |
| `/performance` | **Performance & Web Vitals** | Core Web Vitals (LCP < 2.5s, CLS < 0.1, INP < 200ms), N+1 query elimination, bundle budgets. |
| `/api-design` | **API Contract Design** | OpenAPI 3.1 specifications, RFC 7807 Problem Details error format, idempotency headers. |
| `/observability` | **Distributed Telemetry** | OpenTelemetry distributed tracing, structured JSON logs with correlation IDs, health/ready probes. |
| `/continuous-learning` | **Conversational Learning (CLP)** | Persists project invariants to `.agents/learned_conventions.md` to prevent repeated errors. |
| `/refactor` | **Safe Refactoring** | Strangler Fig pattern, characterization testing, decomposing god files approaching 500 lines. |
| `/git-workflow` | **Git Workflow & Releases** | Git branching, commit chunking (< 1,000 lines), Conventional Commits, release tagging. |

---

## Anti-AI-Slop & Craftsmanship

SkillBuilder actively audits and sanitizes codebases against synthetic AI tropes:
- **No Shields.io Badges**: Eliminates decorative badge spam in documentation and code headers.
- **No Fake Mock Databases**: Prohibits static in-memory toy arrays pretending to be permanent data.
- **No Obvious Comments**: Prohibits restating what code already expresses (`// set loading to true`).
- **No Neon Vibe Aesthetics**: Prohibits neon purple-indigo gradients and glowing border rings.
- **No Emojis as UI Controls**: Replaces raw emojis in buttons/headers with accessible Lucide SVG vector icons.

Audit CLI:
```bash
python3 skills/anti-slop/scripts/sanitize_ai_slop.py --path .
```

---

## Autonomous Research & Fallback Pivots

When a dependency fails to install, exhibits breaking bugs, or is deprecated:
1. **Root Cause Isolation**: Determines if failure is environmental (C++ build tools) or systemic (abandoned library).
2. **Ecosystem Discovery**: Searches actively maintained alternatives across PyPI/npm/Crates.io.
3. **P.A.T.H.S. Trade-Off Evaluation**: Analyzes Performance, Activity, Type Safety, Hygiene (licensing), and Size.
4. **Minimal POC Validation**: Validates candidate in a minimal standalone reproduction before adoption.

Audit CLI:
```bash
python3 skills/research/scripts/research_alternatives.py --query moment
```

---

## Responsiveness QA & Sub-Agent Verification

Ensures applications adapt gracefully across the **4-Tier Viewport Matrix**:
- **Mobile** (`375x667` / `390x844`): Single column, touch targets >= 44x44px, zero horizontal overflow.
- **Tablet** (`768x1024`): Fluid responsive multi-column transitions, collapsible navigation.
- **Desktop** (`1280x800` / `1440x900`): Bounded content containers (`max-w-7xl`), multi-pane dashboards.
- **Widescreen** (`1920x1080+`): Centered layouts without awkward stretching.

Audit CLI:
```bash
python3 skills/qa/scripts/verify_responsiveness_and_qa.py --path .
```

---

## Developer Workspace (`workspace/`)

A dedicated configuration and tooling hub:
- **[`profile.json`](workspace/profile.json)**: Developer metadata, preferred stacks, and token budget preferences.
- **[`pairing_manifesto.md`](workspace/pairing_manifesto.md)**: The 8 non-negotiable tenets of pair-programming.
- **[`prompt_templates/`](workspace/prompt_templates/)**: High-density templates for specifications and bug reproductions.

---

## Continuous Conversational Learning (CLP)

Agents absorb developer corrections and persist them to disk:
```bash
# Record an architectural invariant
python3 skills/continuous-learning/scripts/record_learning.py \
  --category ARCH --text "Use native fetch over axios in all new backend services"

# List all recorded invariants
python3 skills/continuous-learning/scripts/record_learning.py --list
```

---

## Installation & Antigravity Integration

### Universal One-Command Quickstart
```bash
# Install globally for all projects on this workstation
./scripts/install.sh --global

# Or install directly into a specific project repository
./scripts/install.sh --project /path/to/my-project
```

---

## Automated Verification Suites (25 Suites)

SkillBuilder includes a master test runner executing 25 independent verification suites:

```bash
./scripts/verify_all_skills.sh
```

Checks executed:
1. **500-Line Source File Policy**: Verifies all source files adhere to the 500-line limit.
2. **World-Class Engineering Unit Tests**: Validates line-checking and EOS extraction logic.
3. **Anti-AI-Slop Tests**: Validates badge, mock array, and obvious comment sanitization.
4. **Autonomous Research Tests**: Validates package alternative recommendation engine.
5. **Responsiveness QA Tests**: Validates viewport matrix, fixed-width traps, and touch targets.
6. **List-an-Error QA Tests**: Validates Master Error Catalog lookup and classification.
7. **UI Design Tokens Tests**: Validates vector icons, raw emoji bans, and token scales.
8. **UI Frontend Quality Tests**: Validates accessibility and anti-vibe-coding rules.
9. **Frontend Architecture Tests**: Validates lifecycle memory safety and AbortController signals.
10. **Security Defense Tests**: Validates SQL injection defense and secret leak detection.
11. **Fullstack Anti-Mock Tests**: Validates real persistence and boundary schema validation.
12. **Performance & Web Vitals Tests**: Validates N+1 query cascades and CLS image dimensions.
13. **API Design OpenAPI Tests**: Validates OpenAPI 3.1 contracts and status code definitions.
14. **Observability Telemetry Tests**: Validates structured logging and healthcheck endpoints.
15. **Safe Refactoring Tests**: Validates detection of oversized files and deep nesting.
16. **Git Workflow Commit Chunking Tests**: Validates the 1,000-line commit chunk budget.
17. **Continuous Learning Tests**: Validates convention persistence and deduplication.
18. **Backend API Contract Tests**: Validates route contracts and schema validation.
19. **Database Hygiene Tests**: Validates migration safety and non-blocking indexing.
20. **Container DevOps Security Tests**: Validates non-root user and multi-stage container rules.
21. **AI Token Budget Tests**: Validates token calculation and context window budgeting.
22. **Prompt Polish Tests**: Validates intent extraction and filler stripping.
23. **Prompt Polish Learning Tests**: Validates convention indexing.
24. **Production Etiquette Hygiene Tests**: Validates `.env.example`, `.gitignore`, and scaffolding.
25. **Production Etiquette Git Chunk Tests**: Validates git diff partitioning.

---

## Repository Architecture

```text
SkillBuilder/
├── plugin.json                                 # Antigravity plugin manifest (v3.0.0)
├── README.md                                   # Comprehensive documentation & slash command index
├── INTEGRATION_GUIDE.md                        # Step-by-step setup guide for Antigravity
├── AGENTS.md                                   # Root rules enforced on all projects
├── rules/
│   └── AGENTS.md                               # Plugin-level rules
├── workspace/                                  # Developer Workspace & Presets
├── skills/
│   ├── world-class-engineering/                # Master EOS & 500-line ceiling
│   ├── anti-slop/                              # Anti-AI-slop & clean craftsmanship
│   ├── research/                               # Autonomous research & alternative fallbacks
│   ├── qa/                                     # Viewport responsiveness & Master Error Catalog
│   ├── ui/                                     # Design tokens, neutral scales & Lucide icons
│   ├── frontend/                               # React 19, Next.js, Flutter & effect cleanup
│   ├── backend/                                # Clean architecture & Zod/Pydantic validation
│   ├── security/                               # OWASP Top 10, SQL parameterization & secrets
│   ├── fullstack/                              # Anti-mock vertical slices & real persistence
│   ├── database/                               # Zero-downtime migrations & ACID integrity
│   ├── devops/                                 # Multi-stage non-root containers & CI/CD
│   ├── ai/                                     # Gemini SDK, structured JSON & token budgets
│   ├── prompt-polish/                          # Prompt Polishing Engine (PPE)
│   ├── production-etiquette/                   # Resilient network clients & secret hygiene
│   ├── performance/                            # Core Web Vitals & N+1 query elimination
│   ├── api-design/                             # OpenAPI 3.1 & RFC 7807 Problem Details
│   ├── observability/                          # OpenTelemetry tracing & structured JSON logs
│   ├── continuous-learning/                    # Persistent conventions (CLP)
│   ├── refactor/                               # Safe debt remediation & file decomposition
│   └── git-workflow/                           # Atomic commit chunking (<1k lines) & releases
└── scripts/
    ├── install.sh                              # Universal installer (Global / Project)
    └── verify_all_skills.sh                    # Master 25-suite verification test runner
```
