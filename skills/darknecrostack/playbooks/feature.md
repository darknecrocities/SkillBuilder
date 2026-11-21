# Playbook: Feature Implementation

Use when building a new capability, endpoint, UI flow, mascot stage, or vertical slice.

## Steps
1. **Restate Goal & Minimal Scope**: Confirm what changes for the user and prune unnecessary knobs (`Experience First`, `Laziness Protocol`).
2. **Archaeology**: Inspect the nearest existing sibling feature to match repository conventions, helpers, and persistence patterns.
3. **Shape First (`/architect`)**: Lock data shapes, discriminated unions, Zod/Pydantic schemas, DB DDL, API contracts, UI layout hierarchy, and `<250`/`<500`-line file ownership before writing bodies.
4. **Platform Pruning (PDS)**: Mount `/web-ui` OR `/mobile-ui` (never both); mount `/2d-mascot-motion` or `/brand-assets` if visual assets are involved.
5. **Implement Atomically**: Build vertical slice (schema -> repository -> domain -> transport/UI -> tests), keeping functions `<= 40` lines and nesting `<= 3`.
6. **Challenge & Unslop (`/interrogate`)**: Audit diff for edge cases, security/BOLA/SSRF, leaks, and AI slop (`sanitize_ai_slop.py`).
7. **Prove It Works (`/prove-it-works`)**: Run tests, build, and runtime/browser checks on the real artifact.
