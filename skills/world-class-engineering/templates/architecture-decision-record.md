# ADR-[Number]: [Title of Decision]

> **Date**: [YYYY-MM-DD]  
> **Status**: [PROPOSED | ACCEPTED | DEPRECATED | SUPERSEDED by ADR-XXX]  
> **Deciders**: [Architect, Tech Lead, Senior Engineers]  

---

## 1. Context and Problem Statement
[Describe the technical context, business requirements, and operational drivers that make this decision necessary. What problem are we attempting to solve?]

---

## 2. Decision Drivers
- [Driver 1: e.g., Need p95 response time under 100ms]
- [Driver 2: e.g., Strict data residency and compliance rules]
- [Driver 3: e.g., Ease of local development and testing]

---

## 3. Considered Options
1. **Option 1**: [Description]
2. **Option 2**: [Description]
3. **Option 3**: [Description]

---

## 4. Decision Outcome
**Chosen Option**: [Option X], because [justification linking back to decision drivers].

### Positive Consequences
- [Benefit 1: e.g., Eliminates complex distributed transactions]
- [Benefit 2: e.g., High familiarity within existing team stack]

### Negative Consequences & Trade-Offs
- [Trade-off 1: e.g., Requires manual partitioning if table exceeds 100M rows]
- [Trade-off 2: e.g., Additional local Docker dependency for development]

---

## 5. Pros and Cons of Alternatives

### [Option 1: e.g., Microservices with gRPC]
- **Good**: Independent deployment cadence.
- **Bad**: Excessive operational complexity for current team size (4 engineers).

### [Option 2: e.g., Serverless Functions]
- **Good**: Auto-scaling to zero.
- **Bad**: Cold-start latency violates 100ms p95 requirement.

---

## 6. Implementation & Compliance
- [Action item 1: Scaffolding and ADR verification in codebase]
- [Action item 2: Update architecture documentation in `references/architecture.md`]
