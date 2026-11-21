# Firebase Auth, Custom Claims & Admin SDK Security Manual

> **Objective**: Enforce server-side token verification, least-privilege Admin SDK initialization, and tamper-proof custom role claims.

---

## 1. Token Verification & Admin SDK Boundaries

- **Never Trust Client UIDs**: On Cloud Functions (`https.onCall` / HTTP routes) or Next.js API routes, always extract identity from `await getAuth().verifyIdToken(idToken, true)` (`checkRevoked: true` on sensitive mutations!). Never trust `req.body.userId`.
- **Single-Instance Initialization**: Initialize `firebase-admin` once (`getApps().length === 0 ? initializeApp() : getApp()`). Never commit downloaded service account JSON keys into Git (`FIREBASE_SERVICE_ACCOUNT` belongs in Secret Manager or ADC/Workload Identity).

---

## 2. Custom Claims & RBAC Hygiene

- **Keep Claims Compact**: Custom claims live inside the signed JWT (`<= 1,000` bytes max) — store only concise role/tenant keys (`{ role: "editor", tenantId: "t_42" }`), never large arrays or profile fields.
- **Force Token Refresh on Role Change**: After `setCustomUserClaims(uid, ...)`, record a `claimsUpdatedAt` timestamp in Firestore or revoke refresh tokens (`revokeRefreshTokens(uid)`) for demotions so stale permissions cannot linger for 60 minutes.

---

## 3. Emulator-First & Backup Discipline
- Run auth and security-rule integration tests against the **Firebase Emulator Suite** (`firebase emulators:exec`) — never test destructive changes against production data.
- Before altering rules or running bulk Admin SDK migrations, verify a single SHA-256 export slot via `manage_deduplicated_backup.py`.
