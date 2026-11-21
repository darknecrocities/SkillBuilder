# Anti-Slop & Technical Writing Principles

Read these principles before authoring any code comment, README, PR description, commit message, UI copy, or final response.

---

## 1. Unslop Prose & Code
- **When it applies**: Every reply, markdown doc, UI label, and code diff.
- **Rule**: Strip filler intros (*"Certainly! Here's a comprehensive..."*), synthetic marketing fluff (*"revolutionary AI-powered seamless experience"*), decorative `shields.io` badges, speculative unused helpers, and AI visual clichés (purple-pink gradients, 3-card feature soup, neon glow halos, emoji buttons).
- **Style**: Short declarative sentences. Lead with what changed for the user. Avoid em-dash chains and colon connectors where a direct sentence is clearer.

## 2. No Obvious Comments
- **When it applies**: Before review or commit on any source file.
- **Rule**: Delete comments that restate syntax (`// set loading to true`, `# loop through items`). Keep only *why* comments explaining non-obvious invariants, protocol constraints, browser quirks, or ordering dependencies.

## 3. Technical Writing (Docs, Commits & PRs)
- **Rule**:
  - **Commits**: Conventional subject `<type>(<scope>): <imperative summary>` (`<= 72` chars) + blank line + *Context / Key Changes / Verification / Documentation Impact*.
  - **PRs**: Open `## Why` with the user goal, summarize concrete behavioral changes, list exact verified commands + outputs, disclose unverified surfaces, and state `Documentation impact: <files or none — reason>`.

## 4. Candor Over Sycophancy
- **Rule**: Agreement is never the default. When asked to review an approach or add scope that hurts simplicity, contrast, security, or performance, give an honest technical judgment: explain the concrete failure mode or say *"This doesn't earn its place because..."* with a cleaner alternative.
