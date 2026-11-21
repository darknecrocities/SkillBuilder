# Playbook: Opening & Landing a PR (`opening-a-pr`)

Covers `opening-a-pr`, `babysit`, and `shipping` workflows cleanly across GitHub PRs.

## Steps
1. **Pre-Commit Scrub (`/interrogate`)**: Inspect `git diff`, remove obvious comments (`no-comments`), unused imports, and AI slop (`sanitize_ai_slop.py --strict`).
2. **Atomic Commit Budget**: Keep each commit `< 1,000` changed lines with Conventional Title + *Context / Key Changes / Verification / Documentation Impact* body.
3. **Push & Open / Update PR**:
   - `git push -u origin <branch>`
   - `gh pr create --base main --head <branch> --title "..." --body "..."` (or `gh pr edit` if open).
   - PR `## Why` must open with the user's goal; include `## Verification` with exact commands and `[measured]` outputs, plus `Documentation impact: <files or none — reason>`.
4. **Babysit & Judge Bot Comments**: Check CI status (`gh pr checks`) and evaluate automated/human review comments strictly on technical merits before applying fixes.
5. **Ship Clean**: Confirm clean working tree (`git status`), green checks, and up-to-date remote branch.
