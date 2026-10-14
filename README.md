# SkillBuilder: Antigravity Engineering Standards & Production Etiquette Skills

SkillBuilder is a production-grade collection of Agent Skills designed for Google Antigravity. It transforms AI coding agents into disciplined, senior-level software engineers and systems architects by providing concrete operating workflows, architectural constraints, security guardrails, automated project scaffolding, and version-control etiquette.

---

## Table of Contents

1. [Overview & Philosophy](#overview--philosophy)
2. [Skills Included](#skills-included)
   - [Skill 1: world-class-engineering](#1-world-class-engineering)
   - [Skill 2: production-etiquette](#2-production-etiquette)
3. [Automation Scripts & CLI Utilities](#automation-scripts--cli-utilities)
4. [Verification & Testing Suites](#verification--testing-suites)
5. [Installation & Setup](#installation--setup)
   - [Global Installation (All Projects)](#option-a-global-installation)
   - [Project-Level Installation (Team Sharing)](#option-b-project-level-installation)
   - [Mandatory Enforcement via AGENTS.md](#mandatory-enforcement-via-agentsmd)
6. [Repository Structure](#repository-structure)

---

## Overview & Philosophy

Most AI coding assistants generate code without long-term architectural foresight: they exceed maintainable file boundaries, leak credentials, fabricate non-existent API parameters, mock databases with temporary static arrays, and ignore production containerization.

SkillBuilder enforces an uncompromising engineering philosophy:

> Understand first. Plan deliberately. Implement minimally. Test independently. Verify everything. Maintain relentlessly. Real software, real security, real resilience. No toys, no leaked secrets, no unverified assumptions.

---

## Skills Included

### 1. `world-class-engineering`

**Role**: Principal Software Engineer & AI Systems Architect  
**Location**: `skills/world-class-engineering/`

This skill provides comprehensive architectural guidance across frontend, backend, database design, AI/ML engineering, security modeling, and code review.

#### Key Features:
- **The 6-Phase Engineering Operating System (EOS)**:
  - *Phase A: Understand*: Inspect repository structure, package manifests, runtime versions, and existing conventions.
  - *Phase B: Define*: Establish explicit functional, non-functional, security, and error-handling criteria.
  - *Phase C: Plan*: Formulate structured technical designs with data flow diagrams and API contracts.
  - *Phase D: Implement*: Minimal, cohesive, production-ready code reusing established abstractions.
  - *Phase E: Verify*: Execute tests, type checkers, linters, and line-count checks.
  - *Phase F: Deliver*: Transparent reporting of changes, test logs, migration requirements, and known limits.
- **The 500-Line Source File Policy**:
  - Enforces a strict 500 physical line maximum on all source files (`.ts`, `.tsx`, `.js`, `.py`, `.go`, `.rs`, `.java`, `.cs`).
  - Includes a 7-step extraction protocol for safely decomposing oversized files without breaking downstream consumers.
- **The 7 Quality Gates**:
  - Requirements, Architecture, Implementation, Correctness, Security, Maintainability, and Delivery.
- **Supporting References & Templates**:
  - 10 reference guides: `architecture.md`, `clean-code.md`, `full-stack.md`, `ai-engineering.md`, `security.md`, `testing-and-verification.md`, `code-review.md`, `performance.md`, `git-and-change-management.md`, `delivery-checklist.md`.
  - 4 production templates: `implementation-plan.md`, `code-review.md`, `test-plan.md`, `architecture-decision-record.md`.

---

### 2. `production-etiquette`

**Role**: Principal Systems Architect & Production Readiness Engineer  
**Location**: `skills/production-etiquette/`

This skill acts as the day-to-day operational rulebook, automating project hygiene and enforcing non-negotiable standards for secrets, containers, networking, and Git workflows.

#### The 7 Non-Negotiable Pillars:

1. **Automatic Environment & Secrets Hygiene**:
   - Whenever APIs, databases, or tokens are introduced, automatically configure `.env.example`, `.env`, and `.gitignore`.
   - Never commit raw credentials. Enforce boot-time configuration validation with schema validators (Zod, Pydantic).
2. **Standardized Containerization (Docker by Default)**:
   - Provide multi-stage Dockerfiles separating build dependencies from minimal runtime images (`alpine`, `distroless`, `slim`).
   - Run containers strictly as unprivileged non-root users (`USER 10001` / `appuser`).
   - Supply `docker-compose.yml` with explicit dependency health checks (`condition: service_healthy`).
3. **Deep Pre-Planning Research Protocol**:
   - Mandatory empirical investigation of actual code, installed dependencies, lockfiles, and official upstream docs before proposing plans.
   - Eliminates hallucinated API flags, invented library methods, and incorrect runtime assumptions.
4. **Network & Request Resilience**:
   - Mandatory connection and read timeouts on every outbound request (no unbounded network calls).
   - In-memory caching with explicit Time-To-Live (TTL) and mutation-driven cache invalidation.
   - Debouncing on user input fields and throttling on high-frequency event streams.
   - Bounded exponential backoff with full random jitter on transient errors (HTTP 429, 502, 503, 504).
   - Circuit breakers to prevent cascading outages during downstream service failures.
5. **The Anti-Mock / Fully Functional Mandate**:
   - Zero tolerance for "toy demo" code, mock in-memory arrays pretending to be databases, or unlinked UI buttons.
   - All features must implement real schemas, real persistent storage (PostgreSQL, SQLite, structured file stores), real API wiring, and complete error handling.
6. **Continuous Testing & Automated CI/CD**:
   - Every feature and bugfix requires automated unit and integration tests.
   - Standalone GitHub Actions CI workflow (`.github/workflows/ci.yml`) enforcing 5 gates: Linting, Type Checking, Automated Tests, Dependency Security Audit, and Docker Build Verification.
7. **Git Branching, Commit Chunking (< 1k lines), & Ready-to-Review PRs**:
   - Purposeful branch prefixes: `feat/`, `fix/`, `refactor/`, `perf/`, `docs/`, `test/`, `chore/`.
   - The 1,000-line push budget: Decomposing massive diffs into cohesive, atomic commits.
   - Automated PR preparation: Full conventional titles, technical decision summaries, test logs, and rollback procedures.

---

## Automation Scripts & CLI Utilities

Both skills include production-ready, zero-dependency Python 3 CLI utilities located in their respective `scripts/` directories:

### 1. Source Line Limit Validator (`check_source_line_limits.py`)
- **Path**: `skills/world-class-engineering/scripts/check_source_line_limits.py`
- Recursively audits source files for adherence to the 500-line physical limit.
- Automatically excludes package managers, build artifacts, lockfiles, and virtual environments.
- Returns exit code `0` on pass, `1` on violation, and supports `--json` output for CI/CD integration.
- Usage:
  ```bash
  python3 skills/world-class-engineering/scripts/check_source_line_limits.py --path . --verbose
  ```

### 2. Project Hygiene Scaffolder (`scaffold_project_hygiene.py`)
- **Path**: `skills/production-etiquette/scripts/scaffold_project_hygiene.py`
- Audits and auto-scaffolds missing project hygiene files: `.gitignore`, `.env.example`, `Dockerfile`, `.dockerignore`, `docker-compose.yml`, `.github/workflows/ci.yml`, and `.github/pull_request_template.md`.
- Automatically detects project ecosystem (Node.js, Python, Go, or generic).
- Non-destructive: preserves existing user files while filling in missing requirements.
- Usage:
  ```bash
  # Audit project
  python3 skills/production-etiquette/scripts/scaffold_project_hygiene.py --path <project-dir> --check

  # Auto-scaffold missing files
  python3 skills/production-etiquette/scripts/scaffold_project_hygiene.py --path <project-dir> --apply
  ```

### 3. Git Commit Chunk & PR Analyzer (`analyze_git_commit_chunks.py`)
- **Path**: `skills/production-etiquette/scripts/analyze_git_commit_chunks.py`
- Inspects working tree diffs and enforces the 1,000-line review budget.
- Clusters modified files into logical atomic commit chunks (Database, Service, API, UI, Test, Infrastructure).
- Generates Conventional Commit suggestions and ready-to-run GitHub CLI (`gh pr create`) commands with structured descriptions.
- Usage:
  ```bash
  python3 skills/production-etiquette/scripts/analyze_git_commit_chunks.py --path .
  ```

---

## Verification & Testing Suites

Both skills include comprehensive `unittest` test suites verifying the functionality of all CLI tools and resilience wrappers:

```bash
# Test World-Class Engineering tooling:
python3 -m unittest discover -s skills/world-class-engineering/tests -p "test_*.py" -v

# Test Production Etiquette tooling:
python3 -m unittest discover -s skills/production-etiquette/tests -p "test_*.py" -v
```

All 20 unit test cases execute in < 1 second with 100% pass rates.

---

## Installation & Setup

### Option A: Global Installation
To make both skills available across all projects and conversations on your machine:

```bash
mkdir -p ~/.gemini/config/skills

# Copy skills to global configuration
cp -r skills/world-class-engineering ~/.gemini/config/skills/
cp -r skills/production-etiquette ~/.gemini/config/skills/
```

### Option B: Project-Level Installation
To share these skills with your engineering team via Git in any repository:

```bash
# In your project repository:
mkdir -p .agents/skills

# Copy skills into .agents/skills
cp -r /path/to/SkillBuilder/skills/world-class-engineering .agents/skills/
cp -r /path/to/SkillBuilder/skills/production-etiquette .agents/skills/

# Register in .agents/skills.json
cat << 'EOF' > .agents/skills.json
{
  "entries": [
    { "path": ".agents/skills" }
  ]
}
EOF
```

### Mandatory Enforcement via AGENTS.md
To ensure that Antigravity unconditionally follows both skills during every session, add this rule block to your project's root `AGENTS.md` (or globally in your workspace configuration):

```markdown
# Mandatory Engineering Discipline & Production Etiquette

All software architecture, implementation, refactoring, and development tasks MUST strictly adhere to both the `world-class-engineering` and `production-etiquette` skills:

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
   - Maintain a 500-line physical limit on all source files, verified via `check_source_line_limits.py`.
```

---

## Repository Structure

```text
SkillBuilder/
├── README.md                                    # Master documentation (no emojis)
├── AGENTS.md                                    # Mandatory agent rules
├── .gitignore                                   # Standard repository exclusions
├── .agents/
│   └── skills.json                              # Antigravity skill discovery config
└── skills/
    ├── world-class-engineering/
    │   ├── SKILL.md                             # Architecture & EOS workflow
    │   ├── references/                          # 10 architecture & quality guides
    │   ├── templates/                           # 4 design & review templates
    │   ├── scripts/                             # check_source_line_limits.py
    │   └── tests/                               # Line limit validator tests
    └── production-etiquette/
        ├── SKILL.md                             # Operational etiquette workflow
        ├── references/                          # 7 production standards guides
        ├── templates/                           # Docker, CI/CD, resilience templates
        ├── scripts/                             # Hygiene scaffolder & PR analyzer
        └── tests/                               # Scaffolder & PR analyzer tests
```

---

## License

This project is released under the MIT License.