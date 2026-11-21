# Project Architecture Sensing & Manifest Introspection

> **Objective**: Accurately infer a repository's real tech stack, boundaries, and verification gates from manifests and directory topology before minting a project skill.

---

## 1. Manifest & Boundary Discovery Matrix

| Detected Artifacts | Inferred Stack & Boundaries | Key Project-Skill Sections to Mint |
| :--- | :--- | :--- |
| `next.config.*` + `src/app/` | Next.js App Router | Server vs Leaf Client boundaries, static vs dynamic routes, middleware rewrites |
| `pubspec.yaml` + `lib/` | Flutter / Dart | Impeller 120Hz rules, `go_router` routes, `flutter_test` gates |
| `pyproject.toml` + `routers/` | Python / FastAPI | Pydantic v2 boundary schemas, SQLite/Postgres pools, `pytest` / `ruff` |
| `mcp-server/` + `@modelcontextprotocol/sdk` | MCP Server | Transport (`stdio`/`SSE`), `realpath` workspace sandbox, tool schemas |
| `src/data/generated/` | Vendored Data Boundary | Read-only generated JSON rule + typed accessor layer + anti-fabrication status |
| `*.riv` / `assets/mascot*` | Rive / Vector Mascot | Canonical `MascotSM` inputs, `cleanup()` disposal, reduced-motion guard |

---

## 2. Extracting Real Verification Commands

Always read `package.json` (`scripts`), `Makefile`, `pyproject.toml`, and `.github/workflows/*.yml` to extract the **exact** lint, typecheck, smoke, and build commands (`pnpm check:public-data-boundary`, `pnpm search:smoke`, `pytest`, `bash scripts/verify_all_skills.sh`). Never invent nonexistent npm scripts.
