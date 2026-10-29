# Skill Synthesis Protocol (SSP)

The Skill Synthesis Protocol (SSP) mints custom, self-contained project skills under `.agents/skills/<skill-name>/SKILL.md` when a codebase requires unique domain runbooks.

---

## 1. The 4-Stage Synthesis Lifecycle

```text
1. Introspect: Analyze package manifests, Dockerfiles, and custom routing
2. Abstract: Extract recurring architectural idioms and testing patterns
3. Synthesize: Mint standard SKILL.md with progressive disclosure links
4. Register: Append skill entry to .agents/skills.json
```

---

## 2. Structural Requirements for Minted Skills

Every minted project skill must include:
1. Valid YAML frontmatter (`name`, `description`).
2. Philosophy & role definition.
3. Quick Navigation linking to helper scripts and references.
4. Concrete failure mode and testing guardrail.
5. Strictly under 350 physical lines.
