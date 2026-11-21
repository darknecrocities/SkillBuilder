# Token Savings Principles & High-Density Prompt Engineering

> **Objective**: Maximize signal-to-token ratio across system prompts, specs, subagent briefs, and developer responses without losing precision.

---

## 1. Five High-Leverage Token Compression Rules

1. **Platform Domain Specialization (PDS)**: Never send both web (`@container`, View Transitions) and mobile (`SwiftUI`, `Compose`) payloads to the same agent turn (`~1,850` tokens saved per turn).
2. **Progressive Disclosure**: Keep `SKILL.md` under `350` lines as a fast trigger & index; defer deep code recipes, failure tables, and migration guides to `references/`, `principles/`, and `playbooks/`.
3. **Tables Over Prose**: Replace 4-paragraph explanations of parameters, error codes, or variants with compact Markdown tables (`40–60%` fewer tokens, faster LLM attention lookup).
4. **Pointers Over Inline Dumps**: Pass `src/auth/tokenVault.ts#L30-L85` to subagents rather than pasting full files into prompts.
5. **Targeted Diffs & Zero Filler**: Strip conversational preambles (*"Sure! Let's carefully..."*) and unchanged context lines from code output.

---

## 2. Token Budget Benchmarks by Task Tier

| Tier | Target Prompt Context | Active Skills Loaded |
| :--- | :--- | :--- |
| **T1 Bugfix / Surgical** | `< 3,500` tokens | `darknecrostack` + `code-archaeology` + `prove-it-works` |
| **T2 Feature Slice** | `4,000–7,500` tokens | `architect` + domain skill + `interrogate` + `prove-it-works` |
| **T3 Visual / Mascot / Brand** | `4,500–8,000` tokens | `ui` + (`web-ui` OR `mobile-ui`) + `2d-mascot-motion` / `brand-assets` + `anti-slop` |
| **T4 Full-Scale Multi-Track** | Partitioned across workers | `full-scale-mode` coordinator + per-worker `worker.md` |
