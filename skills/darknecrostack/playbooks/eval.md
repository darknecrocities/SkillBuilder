# Playbook: Evaluation (`eval`)

Use when benchmarking prompts, skills, RAG pipelines, local LLMs, or agent workflows.

## Steps
1. **Define Golden Eval Set**: Build deterministic test cases covering happy path, edge cases, adversarial/slop inputs, and failure modes.
2. **Run Baseline First**: Measure baseline pass rate, latency, and token cost before changing prompts or code (`Explain the Number`).
3. **Inspect Failure Modes**: Categorize every failure (missing instruction, wrong tool, schema error, hallucination, contrast/slop violation).
4. **Iterate & Verify**: Apply targeted structural fix (`Encode Lessons in Structure`), re-run full eval set, and report exact before/after `[measured]` scores.
