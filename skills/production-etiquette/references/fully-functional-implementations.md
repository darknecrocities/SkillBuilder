# Fully Functional Implementations & Anti-Mock Standards

This reference governs the non-negotiable requirement for fully functional, real-world implementations, strictly eliminating "toy demos" and fake static data from production code.

---

## 1. The Anti-Mock Mandate

> *Deliver production-grade software, not interactive prototypes.*

A common failure mode in AI-generated code is replacing real software architecture with static mock arrays:
```typescript
// PROHIBITED IN PRODUCTION CODE:
const users = [
  { id: 1, name: "Alice", role: "admin" },
  { id: 2, name: "Bob", role: "user" }
];
export function getUsers() { return users; }
```

In the `production-etiquette` framework, this is strictly forbidden in application source files. Every implementation must be **fully functional**, persistent, and completely wired from interface to storage.

---

## 2. Production vs. Test Fixture Distinction

| Context | Policy | Allowed Implementation |
| :--- | :--- | :--- |
| **Application Source Code** | **Zero Fakes / Zero Static Mocks** | Real database tables, real ORM entities, real schema validation, real persistent storage (SQLite, PostgreSQL, real filesystem writes). |
| **Automated Unit Tests** | **Deterministic Fixtures** | Isolated mock adapters, in-memory SQLite instances, or deterministic HTTP stubs to ensure test speed and isolation. |

---

## 3. Real Persistence Defaults

When building any project that manages data, always supply real persistence:

1. **Relational / SQL Services**:
   - For web apps/APIs: Provide PostgreSQL with migration files, or SQLite (via `better-sqlite3`, `sqlite3`, or `rusqlite`) for zero-configuration standalone apps.
   - Enforce database tables with primary keys, foreign keys, unique constraints, and indices.
2. **File-Based Tooling / CLIs**:
   - For CLI tools that persist state: Use structured atomic file persistence (writing to a temp file and renaming atomically) with JSON/YAML validation.
3. **Real Schema Validation**:
   - Use schema validators (Zod, Pydantic, Joi) to validate and sanitize incoming payloads before inserting into storage.
4. **Complete Error Handling**:
   - Handle real database failure modes: unique constraint violations (`409 Conflict`), record not found (`404 Not Found`), connection timeouts, and transaction deadlocks.

---

## 4. End-to-End Functional Verification

An implementation is considered complete only when:
- [ ] Data submitted via UI or API is physically written to persistent storage.
- [ ] Restarting the application process preserves all previously created data.
- [ ] Error scenarios (duplicate records, invalid types, missing fields) return user-friendly, descriptive error responses.
- [ ] All UI action buttons (submit, delete, update, filter) are fully wired to real endpoints.
