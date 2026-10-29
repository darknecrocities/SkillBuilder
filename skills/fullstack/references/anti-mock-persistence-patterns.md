# Anti-Mock Persistence Standards

The Anti-Mock mandate strictly prohibits static mock arrays pretending to be databases in production or integration code.

---

## 1. Real Persistence Requirements

Requirement | Production Pattern | Prohibited Slop
:--- | :--- | :---
Database Engine | PostgreSQL / SQLite / DuckDB / Prisma | `const users = [{id: 1, name: 'Alice'}, ...]`
Schema Validation | Zod / Pydantic schemas on disk | Unchecked `any` JSON objects
Query Execution | Parameterized SQL / ORM client | In-memory `users.filter(u => u.id === req.id)`
Pre-Mutation Backup | Deduplicated SHA-256 backup | Unrecoverable bulk mutations

---

## 2. In-Memory SQLite for Rapid Real-Persistence Testing

When external database credentials are not yet configured, wire up a real SQLite database rather than a toy array:

```typescript
import Database from 'better-sqlite3';

const db = new Database(':memory:');
db.exec(`
  CREATE TABLE users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
  );
`);
```
