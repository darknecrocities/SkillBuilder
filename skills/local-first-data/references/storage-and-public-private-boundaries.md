# Local-First Storage & Public-Private Data Boundaries Manual

> **Objective**: Guarantee durable, recoverable local storage and airtight boundaries between private research datasets, vendored public exports, and UI routes.

---

## 1. Schema Evolution & Recovery in `IndexedDB` / `SQLite`

1. **Explicit Version Numbers**: Every `IndexedDB` `open(name, version)` and `SQLite` `PRAGMA user_version` must handle incremental `onupgradeneeded` / migration scripts idempotently without wiping existing user records.
2. **Import / Export Checksums**: Local-first apps must support portable JSON/ZIP export with a `schemaVersion` header and pre-import validation (`Zod` / `Pydantic`) before overwriting local stores.
3. **QuotaExceededError Handling**: Wrap `IndexedDB` / `OPFS` / `localStorage` writes in typed quota guards and surface actionable recovery (purge transient caches, prompt export) instead of crashing silently.

---

## 2. Enforcing the Public/Private Data Boundary

```text
[Private Raw Repo / Research] --(Maintainer Sync + Scrub)--> [src/data/generated/*.json (Read-Only)]
                                                                       │
                                                       (ONLY allowed import boundary)
                                                                       ▼
                                                            [src/data/<domain>/*.ts]
                                                                       │
                                                                       ▼
                                                        [App Routes & UI Components]
```

### Boundary Rules
- **No Direct Route Imports of Raw Exports**: Lint/test scripts must reject `import ... from "@/data/generated/..."` inside `src/app/` or `src/components/`. Everything flows through typed accessors (`src/data/<domain>/`) that normalize aliases, filter unpublished statuses, and enforce contracts.
- **Anti-Fabrication Status Enum**:
  ```typescript
  export type RecordVerificationStatus = "VERIFIED" | "PARTIAL" | "NEEDS_RESEARCH";
  ```
  UI views encountering `PARTIAL` or `NEEDS_RESEARCH` render transparent verification notices rather than hiding gaps or inventing numbers.

---

## 3. Offline-First & Local AI Boundary
- Keep prompts, user files, embeddings, and derived caches on-device unless the user explicitly enables a cloud fallback.
- Fail gracefully when local services (e.g., Ollama on `:11434`) are offline: show deterministic offline recovery UI rather than spinning endlessly or silently routing private data externally.
