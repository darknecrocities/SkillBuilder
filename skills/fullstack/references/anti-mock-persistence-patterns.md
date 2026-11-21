# Anti-Mock Persistence Patterns & Local Dev Database Seeding

> **Objective**: Eradicate fake in-memory array state in fullstack apps by making real ephemeral/local persistence effortless in dev, test, and production.

---

## 1. Zero-Friction Real Persistence Choices

| Stack | Local Dev & Test Store | Production Store | Why It Beats Fake Arrays |
| :--- | :--- | :--- | :--- |
| **Node / Next.js** | `better-sqlite3` (`:memory:` in tests, `.data/app.db` in dev) | PostgreSQL (`pg` / Drizzle) or Turso | Enforces real SQL constraints, foreign keys, and migrations |
| **Python / FastAPI** | `sqlite3` / `aiosqlite` (WAL mode) | PostgreSQL (`asyncpg` / SQLAlchemy) | Catches SQL/serialization bugs locally before deploy |
| **Client-Only Offline** | `IndexedDB` / `OPFS` + `Zod` validation | Same (`IndexedDB` / `OPFS`) | Survives page refresh cleanly with real quota/migration handling |

---

## 2. Legitimate Test Seeding vs. Prohibited Mock Arrays

- **PROHIBITED (AI Slop)**: Exporting `let mockUsers = [{ id: 1, name: "Alice" }]` inside `src/services/` or `src/app/api/` and returning `mockUsers.push(newItem)` as the application backend.
- **PRODUCTION STANDARD**:
  1. Run deterministic idempotent seed scripts (`INSERT INTO ... ON CONFLICT DO NOTHING`) against real SQLite/Postgres test databases.
  2. For incomplete external research datasets, expose explicit `RecordVerificationStatus = "VERIFIED" | "PARTIAL" | "NEEDS_RESEARCH"` rather than inventing fake records (`bettersanfernando` rule).
  3. Use MSW (`Mock Service Worker`) **only** inside automated test suites to simulate third-party upstream HTTP dependencies (`Stripe`, `GitHub`), never to fake your own app database.
