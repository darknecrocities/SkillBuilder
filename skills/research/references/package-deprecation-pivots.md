# Package Deprecation & Replacement Matrix

---

## Approved Production Drop-In Alternatives

Deprecated / Problematic | Production Drop-In Replacement | Key Advantages
:--- | :--- | :---
`request` / `urllib3` v1 | `httpx` (Python) / native `fetch` | Async/await, HTTP/2, connection pooling
`moment.js` | `date-fns` / native `Intl` | Zero bundle bloat, tree-shakeable, immutable
`crypto-js` | native `node:crypto` / `Web Crypto API` | Constant-time execution, zero external supply chain risk
`google-generativeai` | `google-genai` | Unified SDK, structured Pydantic schemas, typed tools
`body-parser` | native `express.json()` | Built-in, zero dependency vulnerability
