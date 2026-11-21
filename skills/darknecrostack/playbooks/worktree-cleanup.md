# Playbook: Worktree & Branch Cleanup

Use after merging PRs or finishing parallel subagent worktrees/shares.

## Steps
1. **Verify Landed State**: Confirm target commits are merged or pushed to remote before deleting any local branch or worktree.
2. **Audit Uncommitted Work**: Check `git status` in each worktree; never delete unmerged work without user confirmation.
3. **Prune Cleanly**: Remove temporary `scratch/` test outputs, prune merged local branches (`git branch -d`), and remove stale git worktrees (`git worktree prune`).
4. **Confirm Clean Repo**: Verify `git status -sb` shows clean state on target branch.
