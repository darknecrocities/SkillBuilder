# Autonomous Deep Research Methodology

When encountering deprecated libraries, build tool failures, or novel API architectures, conduct autonomous research before improvising ungrounded workarounds.

---

## 1. Research Progression

1. **Local Introspection**: Read installed package versions, lockfiles, and compiler diagnostic logs.
2. **Official Documentation Search**: Query official SDK docs and migration guides.
3. **Trade-Off Matrix Evaluation**: Compare candidate packages across 4 dimensions:
   - Maintenance Health (recent releases, commit frequency, issue resolution)
   - Performance & Bundle Impact (tree-shaking, memory, cold start)
   - Community Adoption & GitHub Stars
   - Security Audit & CVE History
4. **Drop-In Validation**: Implement minimal reproducible verification script before wide adoption.
