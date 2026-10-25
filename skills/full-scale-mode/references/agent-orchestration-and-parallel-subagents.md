# Parallel Agent Orchestration & Subagent Swarm Architecture

> **Scope**: Protocols for dynamic subagent dispatching, parallel execution streams, file ownership boundaries, structured JSON handoffs, and deterministic parent synthesis in Full-Scale Mode (`/full-scale-mode`).

---

## 1. Master Conductor Philosophy & Authority

In Full-Scale Mode, the primary agent operates as the **Master Conductor**:
1. **Singular Accountability**: Subagents execute delegated tasks, but the primary orchestrator retains 100% accountability for overall system integrity, architecture alignment, and final delivery.
2. **Never Delegate Trivial Work**: Spawning subagents for single-line changes or minor edits incurs unnecessary context overhead. Subagents are reserved for parallelizable, decoupled work streams.
3. **Partitioned File Ownership**: Two concurrent subagents must **never** be assigned to modify the same file simultaneously. Work streams must follow strict domain boundaries.

```mermaid
flowchart TD
    Orchestrator["Master Orchestrator (Primary Agent)"]
    
    Orchestrator -->|Track 3A| S1["Subagent: Backend & Database Engine"]
    Orchestrator -->|Track 3B| S2["Subagent: UI/UX & 3D Sensory Engine"]
    
    Orchestrator -->|Track 4A| S3["Subagent: Security & Resilience Hardener"]
    Orchestrator -->|Track 4B| S4["Subagent: DevOps & Containerization Engine"]
    
    Orchestrator -->|Track 5A| S5["Subagent: Full UI / Viewport Auditor"]
    Orchestrator -->|Track 5B| S6["Subagent: Full App Functional Auditor"]
    
    S1 -.->|Structured JSON Receipt| Orchestrator
    S2 -.->|Structured JSON Receipt| Orchestrator
    S3 -.->|Structured JSON Receipt| Orchestrator
    S4 -.->|Structured JSON Receipt| Orchestrator
    S5 -.->|Structured JSON Receipt| Orchestrator
    S6 -.->|Structured JSON Receipt| Orchestrator
```

---

## 2. Specialized Subagent Role Archetypes

| Archetype | Governing Phase | Primary Responsibilities & Tooling | Boundary Restrictions |
| :--- | :--- | :--- | :--- |
| **System Architect** | Phase 0 & 1 | Requirements analysis, prompt polishing, RFC planning, and ADR authoring. | Read-only analysis; no production code edits. |
| **Research Engine** | Phase 2 | P.A.T.H.S. dependency evaluation, alternative package benchmarking, POC testing. | Sandboxed scratch files only; no production commits. |
| **Backend & Persistence** | Track 3A | Database schemas, ACID transactions, migrations, Zod/Pydantic validation, API routes. | Owns `server/`, `api/`, `db/`, `models/`. Never touches UI components. |
| **UI/UX & Sensory** | Track 3B | Apple HIG tokens, Cupertino materials, hairline lighting, 120Hz compositor, 3D shaders. | Owns `components/`, `styles/`, `views/`. Never touches database schemas. |
| **Security Hardener** | Track 4A | OWASP Top 10 defense, SQL parameterization, secret hygiene (`.env.example`), network timeouts. | Read & patch security surfaces across client and server. |
| **DevOps Specialist** | Track 4B | Non-root multi-stage Dockerfiles (`USER 10001`), docker-compose, CI/CD, OpenTelemetry. | Owns `Dockerfile`, `docker-compose.yml`, `.github/workflows/`. |
| **UI QA Auditor** | Track 5A | 4-tier viewports (375-1920px), safe areas, 44x44pt touch targets, WCAG AA contrast. | Read-only verification via DevTools and responsiveness scripts. |
| **Functional QA Auditor** | Track 5B | State machines, network timeouts, mobile OS lifecycle, memory leaks, Master Error Catalog. | Read-only verification via test suites and functional scripts. |
| **Release Orchestrator** | Phase 6 | Convention recording, commit chunking (<1k lines), semantic tagging, PR generation. | Git tree operations and final walkthrough authoring. |

---

## 3. Structured JSON Inter-Agent Handoff Schema

To prevent token waste and conversational ambiguity, subagents communicate findings, created assets, and test passes using a standardized JSON schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SubagentHandoffPayload",
  "type": "object",
  "required": ["subagent_role", "phase", "status", "files_created", "files_modified", "tests_passed"],
  "properties": {
    "subagent_role": { "type": "string" },
    "phase": { "type": "string" },
    "status": { "type": "string", "enum": ["SUCCESS", "FAILED", "BLOCKED"] },
    "files_created": {
      "type": "array",
      "items": { "type": "string" }
    },
    "files_modified": {
      "type": "array",
      "items": { "type": "string" }
    },
    "exported_symbols": {
      "type": "array",
      "items": { "type": "string" }
    },
    "tests_passed": { "type": "integer" },
    "tests_failed": { "type": "integer" },
    "blockers_or_risks": {
      "type": "array",
      "items": { "type": "string" }
    }
  }
}
```

### Example Subagent Handoff (Track 3A Backend):
```json
{
  "subagent_role": "BackendSpecialist",
  "phase": "Track 3A",
  "status": "SUCCESS",
  "files_created": [
    "src/db/schema/orders.ts",
    "src/api/routes/orders.ts"
  ],
  "files_modified": [
    "src/db/index.ts"
  ],
  "exported_symbols": [
    "orderSchema",
    "createOrderHandler",
    "OrderRepository"
  ],
  "tests_passed": 8,
  "tests_failed": 0,
  "blockers_or_risks": []
}
```

---

## 4. Concurrency Conflict Prevention & Dependency Ordering

When running parallel subagent streams, enforce a two-stage topological order:

```mermaid
flowchart TD
    subgraph Stage1 ["Stage 1: Contract Establishment"]
        BE_Contract["Backend Specialist: Define Schema & API Interface Types"]
    end

    subgraph Stage2 ["Stage 2: Parallel Implementation"]
        BE_Impl["Backend Specialist: Implement Database & Route Handler"]
        UI_Impl["UI/UX Specialist: Build View Components using Interface Types"]
    end

    subgraph Stage3 ["Stage 3: Integration & Global Verification"]
        Master["Master Orchestrator: Wire Route with View & Run 29-Suite QA"]
    end

    BE_Contract --> BE_Impl
    BE_Contract --> UI_Impl
    BE_Impl --> Master
    UI_Impl --> Master
```

### Conflict Prevention Rules:
1. **Contract-First Stabilization**: The backend/data contract (types, interfaces, DTOs) must be committed or written before the UI subagent begins consuming them.
2. **Zero Overlapping Edits**: Never permit Subagent A and Subagent B to write to the same file. If a file requires modifications from both domains (e.g. `App.tsx` or `index.ts`), the primary orchestrator performs the merge after both subagents finish.
3. **Sandbox Workspaces for Exploratory Work**: When a subagent performs deep research or prototype benchmarks, assign it a temporary branch or scratch workspace.

---

## 5. Synthesis & Reconciliation Protocol

Upon receiving handoff payloads from all concurrent subagents, the master orchestrator executes this 4-step reconciliation:
1. **File Limit Check**: Audit all created/modified files against the 500-line physical ceiling.
2. **Contract Alignment Verification**: Verify that symbol names and types exported by Track 3A match what Track 3B consumed.
3. **Global Test Sweep**: Execute `./scripts/verify_all_skills.sh` to confirm no cross-module regressions occurred.
4. **Consolidated Reporting**: Synthesize findings into the user-facing walkthrough without dumping raw intermediate logs.
