# Vertical Slice Architecture & Co-Located Fullstack Delivery

> **Objective**: Ship complete, end-to-end features slice-by-slice (Schema -> Repository -> Service -> API -> UI -> Test) instead of disconnected horizontal stubs.

---

## 1. Anatomy of a Production Vertical Slice

Organize feature slices cleanly under cohesive boundaries (`<= 250–350` lines/file):

```text
src/features/tasks/
├── schema.sql               # DDL migration with CHECK constraints & indexes
├── task.contracts.ts        # Shared Zod schemas & discriminated state types
├── task.repository.ts       # Parameterized SQLite/Postgres queries (tenant-scoped)
├── task.service.ts          # Pure business rules & idempotency coordination
├── task.route.ts            # HTTP/Server Action boundary -> RFC 7807 errors
├── TaskWorkspace.tsx        # Platform-specialized UI (/web-ui or /mobile-ui)
└── task.integration.test.ts # Real DB round-trip test (zero mock arrays)
```

---

## 2. Slice Execution Invariants

1. **Contract-First (`/architect`)**: Author `task.contracts.ts` and `schema.sql` first so server and client share identical types.
2. **Real Persistence (`/anti-slop`)**: Every slice writes to and reads from real SQLite/Postgres/IndexedDB — zero `const mockTasks = [...]` stubs.
3. **Optimistic UI with Honest Failure**: Update UI optimistically via `useOptimistic` / TanStack Query `onMutate`, and roll back with accessible `role="alert"` feedback if the server rejects.
4. **Public/Private Boundary (`bettersanfernando` Pattern)**: If a slice displays curated civic/reference datasets, consume strictly via a typed read-only accessor (`src/data/<domain>/`) and mark incomplete source fields `PARTIAL` / `NEEDS_RESEARCH`.
5. **Proof Before Done**: Integration test MUST `POST` / `PATCH` through the route handler and assert the persisted row inside the database.
