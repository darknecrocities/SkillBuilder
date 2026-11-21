# Playbook: Authoring a Skill (`authoring-a-skill`)

Use when minting or upgrading any skill in `skills/` or `.agents/skills/` (prevents stub decay and boilerplate bloat).

## Steps
1. **Verify Non-Overlap**: Check existing skills first; never duplicate an existing skill domain.
2. **Design Progressive Disclosure Split**:
   - `SKILL.md` (`120–320` lines, hard cap `350`): Trigger rules, workflow steps, decision matrix, CLI commands, and links to `references/`.
   - `references/*.md` (`80–250` lines each): Concrete patterns, bad-vs-good code diffs, failure catalogs, edge-case tables. Zero copy-paste boilerplate across headings.
   - `scripts/*.py` + `tests/*.py`: Deterministic validator/generator CLI + unit tests (`<=500` lines/file).
3. **Lint & Benchmark**: Run `python3 scripts/skill_linter.py --skill <name> --benchmark --strict-depth`.
4. **Sync Multi-Platform Exports**: Run `export_multiplatform.py --repo . --target . --platform all` and register tests in `verify_all_skills.sh`.
