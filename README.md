# SkillBuilder: World-Class Antigravity Engineering & Pair-Programming Skills

[![Verification Status](https://img.shields.io/badge/verification-11%2F11%20passing-brightgreen.svg)](scripts/verify_all_skills.sh)
[![Line Ceiling](https://img.shields.io/badge/source%20files-%3C%20500%20lines-blue.svg)](skills/world-class-engineering/scripts/check_source_line_limits.py)
[![Antigravity](https://img.shields.io/badge/google-antigravity-orange.svg)](INTEGRATION_GUIDE.md)
[![Author](https://img.shields.io/badge/author-Arron%20Kian%20Parejas%20(@darknecrocities)-purple.svg)](arronkianparejas/profile.json)

**SkillBuilder** is a production-grade collection of Agent Skills and engineering guardrails designed for **Google Antigravity**. Crafted specifically for **Arron Kian Parejas (@darknecrocities)** and scalable to engineering teams worldwide, it transforms AI coding assistants into disciplined senior architects and pair programmers.

---

## Table of Contents

1. [Overview & Philosophy](#overview--philosophy)
2. [Arron's Personal Workspace (`arronkianparejas/`)](#arrons-personal-workspace-arronkianparejas)
3. [The 9 Production Skills](#the-9-production-skills)
4. [Prompt Polishing Engine (PPE)](#prompt-polishing-engine-ppe)
5. [Token Savings & High-Density Pairing](#token-savings--high-density-pairing)
6. [QA Testing & Master Error Catalog](#qa-testing--master-error-catalog)
7. [Installation & Antigravity Integration](#installation--antigravity-integration)
8. [Automated Verification Suites](#automated-verification-suites)
9. [Repository Architecture](#repository-architecture)

---

## Overview & Philosophy

Most AI coding assistants suffer from structural myopia: they hallucinate parameters, mock databases with temporary static arrays, leak credentials into version control, exceed maintainable file boundaries, and burn thousands of tokens on conversational filler.

SkillBuilder enforces an uncompromising engineering standard:

> **Understand first. Polish the prompt. Implement minimally. Test thoroughly. Catalog every error. Deliver real software without waste.**

---

## Arron's Personal Workspace (`arronkianparejas/`)

A dedicated configuration and tooling hub tailored to Arron's project construction workflows and tech stacks:

- **[`profile.json`](arronkianparejas/profile.json)**: Author metadata, preferred stacks (React 19, Next.js, Tailwind v4, Flutter, Node.js, FastAPI, Go, PostgreSQL, Cloud SQL, GCP, Gemini 2.5), and token budget preferences.
- **[`personal_pairing_manifesto.md`](arronkianparejas/personal_pairing_manifesto.md)**: The 6 non-negotiable tenets of pair-programming with Arron.
- **[`prompt_templates/`](arronkianparejas/prompt_templates/)**: High-density templates for feature specifications, bug reproductions, and ADRs.
- **[`scripts/sync_to_global.sh`](arronkianparejas/scripts/sync_to_global.sh)**: One-command sync linking SkillBuilder directly to `~/.gemini/config/plugins/skill-builder`.
- **[`scripts/scaffold_project.sh`](arronkianparejas/scripts/scaffold_project.sh)**: Rapid project scaffolder initializing `.gitignore`, `.env.example`, `.agents/`, and `AGENTS.md`.

---

## The 9 Production Skills

SkillBuilder organizes software engineering into 9 specialized, progressively disclosed skills:

| Skill | Role | Key Capabilities |
| :--- | :--- | :--- |
| **`world-class-engineering`** | Principal Software Engineer | 6-Phase EOS (Understand -> Define -> Plan -> Implement -> Verify -> Deliver), 500-line source file limit, 7 quality gates. |
| **`production-etiquette`** | Production Readiness Engineer | Secrets hygiene (`.env.example`), multi-stage non-root Docker (`USER 10001`), resilient networking (timeouts, retries with jitter), anti-mock mandate. |
| **`prompt-refinement-and-metacognition`** | Principal Prompt Engineer | 5-phase Prompt Polishing Engine (PPE), ambiguity detection, token compression, structured engineering specifications. |
| **`qa-testing-and-error-resolution`** | Principal QA & Reliability Engineer | 4-tier testing trophy (Unit, Integration, Contract, E2E), pre-flight QA gates, Master Error Catalog, List-an-Error (LaE) tracking. |
| **`ui-frontend-engineering`** | Frontend & UI/UX Architect | Tailwind CSS v4 design tokens, Radix UI & shadcn primitives, WCAG 2.2 AA accessibility, Core Web Vitals (LCP, INP, CLS), optimistic state updates. |
| **`backend-systems-engineering`** | Backend Systems Architect | Clean/Hexagonal Architecture, REST/gRPC API design, Zod/Pydantic v2 boundary validation, JWT rotation, idempotency keys, RFC 7807 problem details. |
| **`database-and-datastore-engineering`** | Principal Database Architect | PostgreSQL, SQLite, Cloud SQL, zero-downtime expand-and-contract migrations, non-blocking indexes (`CONCURRENTLY`), PgBouncer connection pooling. |
| **`cloud-devops-infrastructure`** | Cloud & Platform Engineer | GCP Cloud Run, GKE, IAM least-privilege, Secret Manager, distroless containers, 5-gate GitHub Actions CI pipeline, OpenTelemetry tracing. |
| **`ai-and-llm-engineering`** | Principal AI Systems Engineer | Gemini 2.5 Pro/Flash, `google-genai` SDK, Antigravity subagents, schema-enforced structured outputs, defensive tool execution, hybrid RAG. |

---

## Prompt Polishing Engine (PPE)

The user prompt is the foundation of all generated software. Before writing code on complex requests, SkillBuilder automatically runs the **PPE**:

1. **Intent Extraction**: Identifies the core functional deliverable and scope boundary.
2. **Ambiguity & Edge-Case Scan**: Uncovers missing error handling, auth requirements, and state dropouts.
3. **Structured Specification**: Converts narrative thoughts into an RFC-style specification matrix.
4. **Token Compression**: Strips conversational padding and formats requirements into compact tables.
5. **Verification Gate**: Attaches automated verification commands.

CLI Utility:
```bash
python3 skills/prompt-refinement-and-metacognition/scripts/polish_prompt.py --text "build an express api for user auth with jwt"
```

---

## Token Savings & High-Density Pairing

To maximize context window longevity and reduce inference latency:
- **Progressive Disclosure**: Only skill names and descriptions are loaded initially (<300 lines per `SKILL.md`). In-depth guides in `references/` are pulled into context only when needed.
- **Local CLI Execution**: Mechanical checks (line counts, project hygiene, commit chunks, token budgets, error lookups) are executed by fast local Python scripts without spending model tokens.
- **High-Density Formatting**: Eliminates conversational filler in favor of surgical diffs, markdown tables, and precise line links (`file:///...#L10`).

CLI Token Budget Estimator:
```bash
python3 skills/ai-and-llm-engineering/scripts/calculate_token_budget.py --text "Sample system prompt payload"
```

---

## QA Testing & Master Error Catalog

SkillBuilder maintains an encyclopedia of software defects across Frontend, Backend, Database, Cloud, and AI systems. Whenever an error occurs, the **List-an-Error (LaE)** protocol captures:
1. `[Error Signature]`: Exact message and code.
2. `[Root Cause]`: Mechanical explanation.
3. `[Remediation]`: Concrete code patch.
4. `[Regression Test]`: Automated test preventing recurrence.

Search the Master Error Catalog:
```bash
python3 skills/qa-testing-and-error-resolution/scripts/lookup_error.py --query "deadlock"
python3 skills/qa-testing-and-error-resolution/scripts/lookup_error.py --query "hydration" --category frontend
```

---

## Installation & Antigravity Integration

SkillBuilder can be installed globally or per-project. For complete setup details, refer to [`INTEGRATION_GUIDE.md`](INTEGRATION_GUIDE.md).

### One-Command Quickstart
```bash
# Clone repository
git clone https://github.com/darknecrocities/SkillBuilder.git ~/SkillBuilder
cd ~/SkillBuilder

# Install globally for all projects on this machine
bash scripts/install.sh --global

# Or scaffold a specific project repository
bash scripts/install.sh --project /path/to/my-project
```

---

## Automated Verification Suites

SkillBuilder includes a master test runner executing 11 independent verification suites:

```bash
bash scripts/verify_all_skills.sh
```

Checks executed:
1. **500-Line Source File Policy**: Verifies all source files adhere to the 500-line limit.
2. **World-Class Engineering Unit Tests**: Validates line-checking logic and extraction protocols.
3. **Project Hygiene Unit Tests**: Validates `.env.example`, `.gitignore`, and container scaffolding.
4. **Git Commit Chunking Tests**: Validates 1,000-line push budget and cluster analysis.
5. **Prompt Refinement Tests**: Validates intent extraction and filler stripping.
6. **Master Error Catalog Tests**: Validates search index and keyword matching.
7. **Frontend Quality Tests**: Validates automated accessibility (a11y) checks.
8. **Backend Contract Tests**: Validates schema validation linter.
9. **Database Hygiene Tests**: Validates SQL migration safety and hazardous lock checks.
10. **Container Security Tests**: Validates non-root user and multi-stage container rules.
11. **AI Token Budget Tests**: Validates token calculation and payload density estimation.

---

## Repository Architecture

```text
SkillBuilder/
├── plugin.json                                 # Antigravity plugin manifest
├── README.md                                   # Comprehensive documentation
├── INTEGRATION_GUIDE.md                        # Step-by-step setup guide for Antigravity
├── AGENTS.md                                   # Root rules enforced on all projects
├── rules/
│   └── AGENTS.md                               # Plugin-level rules
├── .agents/
│   └── skills.json                             # Discovered skills configuration
├── arronkianparejas/                           # Arron's Personal Workspace
│   ├── profile.json                            # Personal profile and stack defaults
│   ├── personal_pairing_manifesto.md           # Pair-programming standards
│   ├── prompt_templates/                       # High-density prompt templates
│   └── scripts/
│       ├── sync_to_global.sh                   # Symlinks to ~/.gemini/config/plugins/
│       └── scaffold_project.sh                 # Scaffolds new projects with Arron's standards
├── skills/
│   ├── world-class-engineering/                # EOS & 500-line ceiling
│   ├── production-etiquette/                   # Secrets, Docker, CI/CD, Git chunking
│   ├── prompt-refinement-and-metacognition/    # Prompt Polishing Engine & token savings
│   ├── qa-testing-and-error-resolution/        # Testing trophy & Master Error Catalog
│   ├── ui-frontend-engineering/                # UI, Tailwind v4, a11y, Core Web Vitals
│   ├── backend-systems-engineering/            # Clean architecture, APIs, Zod, auth
│   ├── database-and-datastore-engineering/     # Relational design, migrations, indexing
│   ├── cloud-devops-infrastructure/            # GCP, distroless containers, IaC, CI/CD
│   └── ai-and-llm-engineering/                 # Gemini API, structured outputs, RAG
└── scripts/
    ├── install.sh                              # Universal installer (Global / Project)
    └── verify_all_skills.sh                    # Master verification test runner
```