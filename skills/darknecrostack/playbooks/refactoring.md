# Playbook: Safe Refactoring

Use when decomposing bloated files (`>350` lines), paying down technical debt, or unifying duplicated logic.

## Steps
1. **Two-Hat Rule**: Never mix new product behavior with structural refactoring in the same commit.
2. **Pin Behavior First**: Verify existing tests pass; if legacy code lacks coverage, write golden-master characterization tests before moving a line.
3. **Subtract Before Adding**: Delete dead branches, unused exports, and one-caller pass-through wrappers first (`Subtract Before You Add`).
4. **Decompose by Cohesive Boundary**: Split along real domain seams (contracts, repository, service, UI subviews) rather than arbitrary line slicing (`Minimize Reader Load`).
5. **Migrate Callers & Delete Legacy**: Update all callers in one wave and remove deprecated adapters immediately.
6. **Verify Equivalence**: Run full test suite, `check_source_line_limits.py --show-tiers`, and `git diff` review.
