# DarkNecroStack Worker Bootstrap (`worker.md`)

> **MANDATORY SUBAGENT PREAMBLE**: Read this entire file before inspecting code, editing files, or running commands. Slash-command skills loaded by the parent agent do not automatically load inside spawned subagent contexts.

## 1. Your Exact Contract
1. **Goal First**: Restate the assigned goal and your exact file-ownership boundary before writing code.
2. **Strict File Isolation**: Only modify files explicitly assigned in your brief. Never edit shared files owned by sibling workers or delete unrelated changes.
3. **Read Before Writing**: Read the target module, its callers, and nearest existing test pattern before creating new abstractions or helpers.

## 2. Engineering & Code Hygiene Invariants
- **Data Shape First**: Define types, schemas, and illegal-state guards before writing implementation logic.
- **Smallest Correct Diff**: Bias to subtraction. Never add speculative abstractions, wrapper layers, or one-caller helpers.
- **500-Line Physical Ceiling**: Keep every source file `<= 500` lines (target `150–250`), functions `<= 40` lines, nesting depth `<= 3` with early returns.
- **Zero Mocks Pretending to Be Persistence**: Never hardcode `const mockData = [...]` in services, routes, or stores. Use real persistence or explicit `PARTIAL` / `NEEDS_RESEARCH` markers if source data is absent.
- **Zero Silent Error Swallowing**: Never emit empty `catch (e) {}` or `except: pass`. Propagate or serialize structured RFC 7807 / typed errors.
- **No Obvious Comments**: Explain *why* non-obvious invariants exist, never *what* the next line literally executes.

## 3. Anti-Slop UI & Asset Rules (When Touching UI or Assets)
- Never emit raw Unicode emojis inside buttons, tabs, or headings; use semantic Lucide SVG icons (`aria-hidden="true"`).
- Never emit purple-pink hero gradients, fuzzy neon halos (`box-shadow: 0 0 40px ...`), 3-column generic icon card soup, or low-contrast `zinc-500` body copy on dark backgrounds.
- For 2D mascots, never use emojis or blurry raster blobs; use Rive (`.riv`), Lottie, or `<35`-node geometric SVG rigs with `prefers-reduced-motion` support.

## 4. Storage & Destructive Guardrails
- Never execute `DROP`, `TRUNCATE`, unconditioned `DELETE`, `rm -rf`, or `git push --force` without explicit coordinator + user confirmation and a SHA-256 backup entry in `.backups/backup_manifest.json`.
- Never commit secrets or `.env` values. Parameterize all SQL and shell arguments (`shell=False`).

## 5. Mandatory Verification & Handoff Report
You are **not done** when code compiles. Before returning to the parent coordinator:
1. Run the exact test, lint, and line-limit commands covering every file you touched.
2. Inspect `git diff` on your owned files to strip dead code, debug logs, and unrequested edits.
3. Return a dense handoff report containing:
   - **Goal & Outcome**
   - **Files Modified / Created** (with line counts)
   - **Principles Applied** (principle name -> concrete choice changed)
   - **Verified Checks `[measured]`** (exact commands + exit codes + outputs)
   - **Unverified Surfaces / Risks** (honest disclosure of anything not executed)
