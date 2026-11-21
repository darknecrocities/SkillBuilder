# Playbook: Multi-Phase Plan

Use when delivering multi-commit or multi-sprint work that spans schema, backend, frontend, assets, and CI.

## Steps
1. **Define Phase Contracts**: Each phase must leave the repository buildable, lint-clean, and 100% test-green on its own.
2. **Order Dependencies Bottom-Up**: Contracts/Schemas -> Domain/Persistence -> API/Transport -> UI/Assets -> Docs/Exporters.
3. **Budget Every Commit**: Keep each phase commit under `1,000` changed lines (`analyze_git_commit_chunks.py`).
4. **Gate Between Phases**: Run `verify_all_skills.sh` or phase test suite before advancing; record checkpoint in `orchestration_state.json`.
5. **Final Integration Sweep**: Re-run full verification harness after the final phase.
