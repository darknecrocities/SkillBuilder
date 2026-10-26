---
name: firebase
description: Firebase serverless architecture, Cloud Firestore schema design, Security Rules (firestore.rules, storage.rules), Firebase Auth, and Admin SDK.
---

# Firebase Serverless, Firestore & Security Rules (`/firebase`)

> **Philosophy**: *Zero open security rules. Client SDKs are untrusted. Enforce request.auth scoping on every document. Batch writes capped at 500 ops. Atomic transactions for financial balances. Composite indexes for multi-field queries.*

This skill establishes defensive engineering standards for building and deploying applications backed by **Google Firebase** and **Cloud Firestore**.

---

## 1. The Core Firebase Architecture Gates

```mermaid
flowchart TD
    A["Client App Request"] --> B["Gate 1: Firebase Auth & Custom Claims (JWT validation)"]
    B --> C["Gate 2: Firestore Security Rules (Strict Owner Scoping)"]
    C --> D["Gate 3: Composite Indexing (Pre-defined index declarations)"]
    D --> E["Gate 4: Atomic Transactions & Batched Writes (<= 500 ops)"]
    E --> F["Gate 5: Admin SDK Privilege Isolation (Zero client credentials)"]
```

1. **Gate 1: Authentication & Custom Claims**: Verify identity on every client call. Use custom claims (`role`, `tenantId`) in JWT tokens for RBAC.
2. **Gate 2: Zero Open Security Rules**: Prohibit `allow read, write: if true;` under any circumstance. All document access must require `request.auth != null` and match `resource.data.userId == request.auth.uid`.
3. **Gate 3: Composite Indexing**: Declare multi-field queries in `firestore.indexes.json` before deployment to prevent runtime query rejections.
4. **Gate 4: Atomic Transactions & Batch Caps**: Mutating related balances or counters must use `db.runTransaction()`. Batched writes must never exceed the 500 document ceiling.
5. **Gate 5: Admin SDK Privilege Isolation**: Never bundle Firebase Admin SDK service account credentials in client or edge bundles.

---

## 2. Hardened Firestore Security Rules (`firestore.rules`)

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // Helper functions
    function isAuthenticated() {
      return request.auth != null;
    }

    function isOwner(userId) {
      return isAuthenticated() && request.auth.uid == userId;
    }

    function isValidUserPayload() {
      return request.resource.data.keys().hasAll(['email', 'displayName', 'updatedAt'])
        && request.resource.data.email is string
        && request.resource.data.updatedAt == request.time;
    }

    // User profile collection
    match /users/{userId} {
      allow read: if isAuthenticated();
      allow create: if isOwner(userId) && isValidUserPayload();
      allow update: if isOwner(userId) && isValidUserPayload();
      allow delete: if false; // Soft deletes only
    }

    // Tenant-isolated documents
    match /tenants/{tenantId}/documents/{docId} {
      allow read, write: if isAuthenticated() && request.auth.token.tenantId == tenantId;
    }
  }
}
```

---

## 3. Atomic Transactions & Batch Size Hygiene (TypeScript)

```typescript
import { getFirestore, runTransaction, doc } from "firebase-admin/firestore";

const db = getFirestore();

export async function transferBalance(
  fromUserId: string,
  toUserId: string,
  amount: number
): Promise<void> {
  if (amount <= 0) throw new Error("Transfer amount must be positive");

  const fromRef = db.collection("wallets").doc(fromUserId);
  const toRef = db.collection("wallets").doc(toUserId);

  await runTransaction(db, async (transaction) => {
    const fromDoc = await transaction.get(fromRef);
    const toDoc = await transaction.get(toRef);

    if (!fromDoc.exists || !toDoc.exists) {
      throw new Error("One or both wallets not found");
    }

    const currentFromBalance = fromDoc.data()?.balance || 0;
    if (currentFromBalance < amount) {
      throw new Error("Insufficient funds");
    }

    transaction.update(fromRef, { balance: currentFromBalance - amount, updatedAt: new Date() });
    transaction.update(toRef, { balance: (toDoc.data()?.balance || 0) + amount, updatedAt: new Date() });
  });
}
```

---

## 4. Firebase Rules & Hygiene Verification CLI

Audit your repository for insecure Firestore security rules and exposed Admin SDK keys:

```bash
python3 skills/firebase/scripts/verify_firebase_rules.py --path . --strict
```

Audited Rules:
- `FIREBASE-OPEN-WILDCARD-RULE`: Flags open `allow read, write: if true;` rules.
- `FIREBASE-MISSING-AUTH-CHECK`: Flags mutation rules without `request.auth` checks.
- `FIREBASE-EXPOSED-ADMIN-KEY`: Flags committed `firebase-adminsdk` service account JSON keys.
- `FIREBASE-OVERSIZED-BATCH`: Flags unchunked batch operations exceeding 500 writes.
