# Connection Pooling & Transaction Management

Protecting database stability under concurrent traffic.

---

## 1. Connection Pool Sizing
Database connections consume RAM and operating system threads. A common anti-pattern is allocating 100 connections per container instance, quickly exhausting database memory.

Follow PostgreSQL's sizing heuristic:
$$\text{Pool Size} = (2 \times \text{CPU Cores}) + \text{Disk Spindles}$$

For containerized cloud microservices (e.g. Cloud Run, GKE), place an intermediate connection pooler (**PgBouncer** or **Google Cloud SQL Auth Proxy**) in transaction pooling mode.

---

## 2. Transaction Isolation Levels
- **Read Committed** (Default): Protects against dirty reads.
- **Repeatable Read**: Protects against non-repeatable reads. Use when reading consistent point-in-time snapshots for reporting.
- **Serializable**: Maximum safety. Rolls back on any serialization anomaly. Requires application retry loops.
