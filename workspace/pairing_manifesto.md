# Developer Pairing Manifesto

> *"Understand first. Polish the prompt. Learn continuously. Reject vibe coding. Implement minimally. Test thoroughly. Catalog every error. Deliver real software without waste."*

This document defines how AI agents and collaborators must pair-program on any project. These principles are mandatory and govern all interactions, planning phases, code generations, and deliveries.

---

## The 8 Non-Negotiable Tenets of Pair Programming

### 1. Mandatory Prompt Polishing Before Execution
- When the developer provides a prompt, feature request, or raw notes, do **not** jump directly into speculative code generation.
- Execute the **Prompt Polishing Engine (PPE)**:
  - Extract the core intent.
  - Detect ambiguities and missing constraints.
  - Structure into a high-density, token-efficient engineering specification.
  - Define clear acceptance and verification criteria.
- Only execute once goals and boundaries are crystal clear.

### 2. Continuous Conversational Learning (CLP)
- **Absorb corrections immediately**: When the developer corrects a style, framework, or architectural choice, acknowledge it and persist it to `.agents/learned_conventions.md` using `scripts/record_learning.py`.
- **Never repeat corrected mistakes**: Once an invariant is recorded, subsequent turns and sessions must strictly comply without requiring reminders.

### 3. Anti-Vibe-Coding UI Craftsmanship
- **Reject AI aesthetic tropes**:
  - Prohibit neon purple/indigo gradients.
  - Prohibit neon green/cyan glow borders (`shadow-[0_0_...`).
  - Prohibit "card-soup" layouts (nesting cards inside cards with heavy elevation).
  - Prohibit decorative badges ("v1.0.0-beta", "AI-Powered").
  - Prohibit synthetic marketing buzzwords in UI copywriting.
- **Iconography over emojis**: Strictly prohibit using raw emojis in buttons, navigation, and headings. Always use semantic SVG vector icons (Lucide Icons) with `aria-hidden="true"`.
- **Palette**: Use high-contrast, disciplined neutrals (zinc/slate) with subtle 1px borders.

### 4. The Anti-Mock / Fully Functional Mandate
- **Zero static toy arrays**: Never mock databases or state with temporary in-memory arrays pretending to be permanent.
- **Real persistence**: Every feature must connect to real persistence (SQLite, PostgreSQL, Cloud SQL, or structured file storage).
- **Full end-to-end integration**: UI buttons must trigger real handlers; handlers must call real APIs; APIs must execute real queries.

### 5. Radical Token Savings & High-Density Communication
- Optimize for high information density per token.
- Avoid pleasantries, conversational padding, and echoing the user prompt back.
- Use structured diffs, exact file references (`file:///...`), markdown tables, and compact code blocks.
- Offload mechanical validations to local CLI scripts (`scripts/`) rather than burning LLM context window tokens.

### 6. Continuous Verification & QA Before Delivery
- Never claim that code works, builds, or passes tests without inspecting the real execution output.
- Every change must pass:
  1. Static type checking (TypeScript `tsc`, Python `mypy`/`pyright`).
  2. Linter checks (ESLint, Ruff).
  3. Automated unit and integration tests.
  4. The **500-line source file policy** via `check_source_line_limits.py`.

### 7. Proactive "List an Error" (LaE) Logging
- Whenever a failure, bug, or exception occurs during development, classify and catalog it:
  - **[Error Signature]**: Exact message and code.
  - **[Root Cause]**: Why it failed.
  - **[Remediation]**: Concrete code diff or config fix.
  - **[Regression Test]**: Automated test guaranteeing it cannot recur.

### 8. Atomic Git Commits Under 1,000 Lines
- Break large changes into cohesive, single-purpose commits.
- Never push an unreviewed massive diff exceeding 1,000 lines.
- Ensure every commit compiles and passes tests independently.
