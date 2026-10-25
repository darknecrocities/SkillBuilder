# Token Savings & High-Density Engineering Principles

In large-scale agentic pair programming, tokens represent latency, cost, and context window exhaustion. Maximize efficiency with these non-negotiable principles.

---

## 1. Eliminate Conversational Overhead
- **Bad**: "Sure! I would be more than happy to help you build this feature. Here is a step-by-step guide explaining how we can do it..."
- **Good**: "Drafting technical design and implementing feature with test coverage."

## 2. Progressive Disclosure
- Never inject 2,000 lines of documentation into the prompt by default.
- Keep `SKILL.md` under 300 lines with high-level tables.
- Defer deep guides to `references/` and load them only when the task requires it.

## 3. High-Density Data Representation
- Use markdown tables instead of verbose repetitive paragraphs.
- Use unified diffs instead of reprinting full 400-line files for a 3-line change.

## 4. Local Execution Over In-Context Computation
- Offload mechanical tasks to local CLI scripts:
  - Checking line limits -> `check_source_line_limits.py`
  - Scaffolding project hygiene -> `scaffold_project_hygiene.py`
  - Analyzing commit chunks -> `analyze_git_commit_chunks.py`
  - Searching errors -> `lookup_error.py`

## 5. Token Savings Checklist
- [ ] No conversational preamble or postamble.
- [ ] Code changes presented as surgical diffs or targeted replacements.
- [ ] Exact line links used (`file:///path#L10-L20`).
- [ ] Documentation loaded on demand.
