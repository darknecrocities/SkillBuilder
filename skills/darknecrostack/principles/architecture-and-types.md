# Architecture & Type System Principles

Read these principles when designing state, API/tool boundaries, typed signatures, migrations, or concurrent workflows.

---

## 1. Model the Domain
- **When it applies**: Writing stateful logic, branching workflows, or code repeating shape assumptions across multiple files.
- **Rule**: Encode the domain in a structured model — a finite state machine, discriminated union, lookup table, reducer, or typed registry — rather than scattered `if/else` flags (`isLoading && !isError && hasData`).
- **Litmus Test**: Impossible state combinations cannot even be constructed.

## 2. Boundary Discipline
- **When it applies**: Wiring HTTP/MCP inputs, form submissions, environment variables, local storage reads, or framework adapters.
- **Rule**: Parse and validate untrusted data once at the outer system boundary (Zod, Pydantic v2, JSON Schema), transform it into trusted domain types, and keep core domain logic 100% pure and framework-free.
- **Litmus Test**: Internal domain functions never re-parse raw strings or inspect HTTP request objects.

## 3. Type System Discipline
- **When it applies**: Designing interfaces, schemas, or function signatures in TypeScript, Python, Swift, Kotlin, Dart, Go, or Rust.
- **Rule**: Make illegal states unrepresentable. Brand primitive IDs (`UserId`, `TenantId`) where mix-ups cause security/BOLA bugs, forbid `any` / untyped `dict` leakage across boundaries, and constrain enums/unions explicitly.

## 4. Make Operations Idempotent
- **When it applies**: Designing CLI generators, migrations, backups, webhooks, queue consumers, or retryable loops.
- **Rule**: Re-running the same operation twice on crashes or retries must converge to the exact same end state without duplicating records, spamming `.bak.1` files, or corrupting indexes.

## 5. Migrate Callers Then Delete Legacy APIs
- **When it applies**: Replacing an internal API, hook, or schema while old callers still exist.
- **Rule**: Migrate every caller in one coordinated wave (or explicit Strangler Fig sequence) and immediately delete the deprecated API and tests so dead dual-paths do not fossilize.

## 6. Separate Before Serializing Shared State
- **When it applies**: Concurrent subagents, background workers, or parallel threads touching files, git branches, caches, or database rows.
- **Rule**: Eliminate sharing first via partitioned file ownership, isolated worktrees/branches, or tenant-scoped keys. Only introduce locks/queues (`backup_manifest.json`, DB `SELECT FOR UPDATE`) for the minimal truly shared resource.
