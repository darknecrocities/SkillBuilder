# The 5-Phase Prompt Polishing Framework

This guide details how to transform raw user ideas into production-ready engineering specifications.

---

## Phase 1: Intent Extraction

When an engineer says:
> *"I need a chat feature for my app with instant messages and history."*

Extract:
1. **Primary Intent**: Real-time bidirectional chat interface with message persistence and historical retrieval.
2. **Implied Architecture**: WebSocket / SSE for real-time delivery, database table for message history, REST endpoint for historical pagination.
3. **Core Entities**: `User`, `Conversation`, `Message`.

---

## Phase 2: Edge-Case & Ambiguity Discovery

Analyze missing boundary conditions:
- **Connection Drops**: How does the UI handle reconnection and backoff?
- **Ordering**: How are concurrent messages sorted (monotonically increasing IDs or server timestamps)?
- **Pagination**: Limit/offset vs cursor-based pagination?
- **Authentication**: How are WebSocket connections authenticated (JWT in handshake query/header)?

---

## Phase 3: Structured Formulation

Convert the narrative into an RFC-style specification:
- **Actors**: Sender, Receiver, Message Broker, Database.
- **Data Flow**:
  1. Client sends message via WebSocket frame.
  2. Server validates payload via schema (Zod/Pydantic).
  3. Server persists message in database.
  4. Server broadcasts message to recipient connection pool.
  5. Client updates UI optimistically.

---

## Phase 4: Token Optimization

Reduce token waste by:
- Replacing conversational phrases with bulleted constraints.
- Using Markdown tables for field definitions.
- Referencing existing files by path instead of pasting entire files.

---

## Phase 5: Verification Criteria

Attach verifiable gates:
- Unit test for payload validation (valid vs invalid frames).
- Integration test for WebSocket handshake and message broadcast.
- Automated check for line count compliance (< 500 lines).
