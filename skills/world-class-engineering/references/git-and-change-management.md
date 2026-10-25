# Git and Change Management Standards

This reference guides version control discipline, working tree hygiene, non-destructive workflows, and commit conventions.

---

## 1. Working Tree Hygiene

Before executing any file modifications or git commands:

1. **Inspect Working Tree State**:
   ```bash
   git status
   git diff --stat
   ```
2. **Preserve User Modifications**:
   - Check whether uncommitted modifications belong to the current task or unrelated user work.
   - **Never** run destructive operations like `git reset --hard`, `git checkout -- .`, `git clean -fd`, or `git restore .` without explicit user permission.
   - If uncommitted changes conflict with the planned task, ask the user whether to stash them (`git stash save "wip"`) or keep them.

---

## 2. Non-Destructive Operations & History Protection

- **No Unauthorized Force Pushes**: Never execute `git push --force` or `git push --force-with-lease` to remote branches unless explicitly instructed by the user.
- **Never Rewrite Shared History**: Avoid rebasing commits that have already been pushed to shared team branches (e.g., `main`, `master`, `develop`).
- **Atomic Commits**: Group related changes into single, cohesive commits that pass all tests and builds independently. Do not bundle unrelated refactors, dependency updates, and feature changes into a single sprawling commit.

---

## 3. Commit Message Standards (Conventional Commits: Title + Description)

Format commit messages using the standard **Conventional Commits** specification with **mandatory Title AND Description Body**:

```text
<type>(<optional scope>): <short summary in imperative mood under 72 chars>

- Context / Why: Problem statement, motivation, or requirement driving the change.
- Key Changes / What: Bulleted breakdown of affected modules, schemas, and files.
- Verification / Impact: Exact automated test commands executed and guardrail receipts.

[optional footer(s), e.g., Closes #123]
```

### Commit Types
- `feat`: A new user-facing feature.
- `fix`: A bug fix.
- `refactor`: Code change that neither fixes a bug nor adds a feature.
- `perf`: A code change that improves performance.
- `test`: Adding or correcting tests.
- `docs`: Documentation-only changes.
- `chore`: Maintenance tasks, dependency bumps, tooling updates.

### Good Commit Message Example
```text
feat(billing): add stripe webhook signature validation

- Context / Why: Prevent webhook replay and signature spoofing attacks.
- Key Changes / What:
  * Implement HMAC-SHA256 signature verification in webhook handler
  * Add test coverage for valid, tampered, and expired signatures
  * Introduce STRIPE_WEBHOOK_SECRET to environment configuration
- Verification / Impact: 12 webhook unit tests passing; all files under 500 lines.

Closes #412
```

---

## 4. Branching, Remote Push & PR Lifecycle

- **Short-Lived Feature Branches**: Branch names must be descriptive and prefixed by purpose (e.g., `feat/oauth-login`, `fix/cart-race-condition`, `chore/bump-deps`).
- **Always Push to the Remote Branch**: Every commit must be pushed immediately to `origin <branch-name>`. Never leave unpushed local commits.
- **Always Open or Update a Pull Request**: Every feature or phase completion must author or update an active, ready-to-merge GitHub Pull Request (`gh pr create` / `gh pr edit`).
- **PR Description Hygiene**:
  - State the problem being solved.
  - Summarize the architectural approach and key trade-offs.
  - List all modified and created files.
  - Provide instructions for verification and testing.
  - Document any required environment variables, database migrations, or breaking changes.
