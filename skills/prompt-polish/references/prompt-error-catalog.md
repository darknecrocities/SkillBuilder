# Prompt Error Catalog & Resolution Guide

A structured index of common prompt defects, their root causes, and corrective actions.

---

### PRM-ERR-001: Ambiguous Boundary Specification
- **Symptom**: User asks to "make a dashboard" without specifying data sources, authentication, or rendering framework.
- **Root Cause**: Missing functional boundaries and architectural context.
- **Remediation**:
  1. Halt immediate coding.
  2. Ask targeted multiple-choice question: Framework (Next.js vs Vite), Auth (JWT vs Session), Data (Mock vs PostgreSQL).
  3. Propose standard default (Next.js App Router + PostgreSQL) and proceed if confirmed.

---

### PRM-ERR-002: Contradictory Architectural Constraints
- **Symptom**: User requests "fully serverless single-file script that maintains a long-running WebSocket server and local SQLite database".
- **Root Cause**: Incompatible runtime primitives (ephemeral serverless execution vs persistent stateful connections).
- **Remediation**:
  1. Highlight architectural collision clearly.
  2. Propose containerized deployment (e.g. Cloud Run with minimum 1 instance or Docker container).

---

### PRM-ERR-003: Conversational Token Bloat
- **Symptom**: Prompts laden with polite pleasantries, redundant restatements of context, and non-actionable background stories.
- **Root Cause**: Natural human conversational typing patterns.
- **Remediation**:
  1. Run `scripts/polish_prompt.py` to distill into compact requirements matrix.
  2. Strip conversational noise, leaving only goal, constraints, schema, and verification rules.

---

### PRM-ERR-004: Missing Failure & Error Handling Criteria
- **Symptom**: Prompt specifies happy path only ("user logs in and gets redirected") with no mention of invalid passwords, account lockouts, or rate limits.
- **Root Cause**: Optimistic bias in specification drafting.
- **Remediation**:
  1. Inject standard 3-tier error handling (client validation, server business exceptions, network timeout fallback).
