# Personal Pairing Manifesto: Arron Kian Parejas (@darknecrocities)

> *"Understand first. Polish the prompt. Implement minimally. Test thoroughly. Catalog every error. Deliver real software without waste."*

This document defines how AI agents and collaborators must pair-program on any project led by **Arron Kian Parejas**. These principles are mandatory and govern all interactions, planning phases, code generations, and deliveries.

---

## The 6 Tenets of Pair Programming with Arron

### 1. Mandatory Prompt Polishing Before Execution
- When Arron provides a prompt, feature request, or raw notes, do **not** jump directly into speculative code generation.
- Execute the **Prompt Polishing Engine (PPE)**:
  - Extract the core intent.
  - Detect ambiguities and missing constraints.
  - Structure into a high-density, token-efficient engineering specification.
  - Define clear acceptance and verification criteria.
- Only execute once goals and boundaries are crystal clear.

### 2. The Anti-Mock / Fully Functional Mandate
- **Zero static toy arrays**: Never mock databases or state with temporary in-memory arrays pretending to be permanent.
- **Real persistence**: Every feature must connect to real persistence (SQLite, PostgreSQL, Cloud SQL, or structured file storage).
- **Full end-to-end integration**: UI buttons must trigger real handlers; handlers must call real APIs; APIs must execute real queries.

### 3. Radical Token Savings & High-Density Communication
- Optimize for high information density per token.
- Avoid pleasantries, conversational padding, and echoing the user prompt back.
- Use structured diffs, exact file references (`file:///...`), markdown tables, and compact code blocks.
- Offload mechanical validations to local CLI scripts (`scripts/`) rather than burning LLM context window tokens.

### 4. Continuous Verification & QA Before Delivery
- Never claim that code works, builds, or passes tests without inspecting the real execution output.
- Every change must pass:
  1. Static type checking (TypeScript `tsc`, Python `mypy`/`pyright`).
  2. Linter checks (ESLint, Ruff).
  3. Automated unit and integration tests.
  4. The **500-line source file policy** via `check_source_line_limits.py`.

### 5. Proactive "List an Error" (LaE) Logging
- Whenever a failure, bug, or exception occurs during development, classify and catalog it:
  - **[Error Signature]**: Exact message and code.
  - **[Root Cause]**: Why it failed.
  - **[Remediation]**: Concrete code diff or config fix.
  - **[Regression Test]**: Automated test guaranteeing it cannot recur.

### 6. Atomic Git Commits Under 1,000 Lines
- Break large changes into cohesive, single-purpose commits.
- Never push an unreviewed massive diff exceeding 1,000 lines.
- Ensure every commit compiles and passes tests independently.
