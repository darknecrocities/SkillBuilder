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
5. [Installation & Setup in Google Antigravity](#installation--setup-in-google-antigravity)
   - [Method 1: Global Plugin Setup (Recommended)](#method-1-global-plugin-setup-recommended---automatic-for-all-projects)
   - [Method 2: Project-Level Setup (Team Sharing)](#method-2-project-level-setup-team-sharing-via-version-control)
   - [Method 3: Standalone On-Demand Skills](#method-3-standalone-on-demand-skills-no-always-on-enforcement)
   - [Troubleshooting & FAQ](#troubleshooting--faq)
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

---

## Installation & Setup in Google Antigravity

Follow one of the setup methods below depending on whether you want machine-wide automatic enforcement or per-repository team sharing.

### Method 1: Global Plugin Setup (Recommended - Automatic for All Projects)

This is the fastest and most complete setup. It registers SkillBuilder as a machine-wide Antigravity plugin. Antigravity will automatically load the skills and enforce the rules across **every current and future project** on your computer.

#### Step 1: Clone the Repository into Antigravity Plugins Directory

- **macOS / Linux**:
  ```bash
  git clone https://github.com/darknecrocities/SkillBuilder.git ~/.gemini/config/plugins/skill-builder
  ```

- **Windows (PowerShell)**:
  ```powershell
  git clone https://github.com/darknecrocities/SkillBuilder.git $HOME\.gemini\config\plugins\skill-builder
  ```

#### Step 2: How It Operates Inside Antigravity
Once cloned into the plugins directory:
1. Antigravity automatically detects `plugin.json` and activates the `skill-builder` plugin.
2. The rules in `rules/AGENTS.md` are automatically merged into Antigravity's active rule set, executing on **every conversation turn**.
3. Both `world-class-engineering` and `production-etiquette` skills are registered and available in the skill catalog.

#### Step 3: Verify the Installation
1. Start Antigravity or open a new conversation.
2. Send this test prompt to the agent:
   ```text
   What engineering standards and active skills are configured in this session?
   ```
   The agent will respond confirming that `world-class-engineering` and `production-etiquette` are active, and cite the mandatory 8-rule etiquette policy.

#### Step 4: Updating to the Latest Standards
To pull new guidelines, templates, or bugfixes in the future:
```bash
cd ~/.gemini/config/plugins/skill-builder && git pull
```

---

### Method 2: Project-Level Setup (Team Sharing via Version Control)

Use this method if you want to commit these standards directly into a specific project repository so that every engineer and agent on your team shares the exact same rules.

#### Step 1: Copy Skills and Rules into Your Project Root
In your project repository:
```bash
# 1. Create the Antigravity agent directories
mkdir -p .agents/skills

# 2. Copy the skills into .agents/skills/
cp -r /path/to/SkillBuilder/skills/* .agents/skills/

# 3. Copy the mandatory rules to the repository root
cp /path/to/SkillBuilder/AGENTS.md ./AGENTS.md
```

#### Step 2: Register Skills in `.agents/skills.json`
Create or update `.agents/skills.json` at the root of your project:
```json
{
  "entries": [
    {
      "path": ".agents/skills"
    }
  ]
}
```

#### Step 3: Commit to Git
```bash
git add .agents/ AGENTS.md
git commit -m "chore: configure Antigravity world-class engineering and production etiquette standards"
git push
```
Any teammate opening this repository with Antigravity will automatically inherit these rules.

---

### Method 3: Standalone On-Demand Skills (No Always-On Enforcement)

If you only want these skills available in your Antigravity catalog on demand without forcing them on every turn:

- **macOS / Linux**:
  ```bash
  mkdir -p ~/.gemini/config/skills
  git clone https://github.com/darknecrocities/SkillBuilder.git /tmp/skillbuilder
  cp -r /tmp/skillbuilder/skills/* ~/.gemini/config/skills/
  rm -rf /tmp/skillbuilder
  ```

- **Windows (PowerShell)**:
  ```powershell
  mkdir -Force $HOME\.gemini\config\skills
  git clone https://github.com/darknecrocities/SkillBuilder.git $env:TEMP\skillbuilder
  Copy-Item -Recurse $env:TEMP\skillbuilder\skills\* $HOME\.gemini\config\skills\
  Remove-Item -Recurse -Force $env:TEMP\skillbuilder
  ```

---

### Troubleshooting & FAQ

#### Why is the agent not automatically applying the skills in my prompts?
Skills in Antigravity use progressive disclosure: their full instructions are only read when requested or triggered. To make them mandatory on every turn, ensure `rules/AGENTS.md` is present in `~/.gemini/config/plugins/skill-builder/rules/AGENTS.md` (Method 1) or in your project's root `AGENTS.md` (Method 2).

#### Do I need to restart Antigravity after installing?
If you are currently in an active conversation, simply start a new conversation or restart Antigravity so it re-indexes newly installed plugins and rules.

#### How do I run the Python tools manually?
All tools use only Python 3 standard library modules:
```bash
# Audit 500-line limits
python3 ~/.gemini/config/plugins/skill-builder/skills/world-class-engineering/scripts/check_source_line_limits.py --path .

# Audit project hygiene (.env, Dockerfile, CI/CD)
python3 ~/.gemini/config/plugins/skill-builder/skills/production-etiquette/scripts/scaffold_project_hygiene.py --path . --check

# Analyze diff budget (< 1k lines) and generate PR descriptions
python3 ~/.gemini/config/plugins/skill-builder/skills/production-etiquette/scripts/analyze_git_commit_chunks.py --path .
```

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