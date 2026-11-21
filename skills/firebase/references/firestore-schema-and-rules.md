# Firestore Schema Design, Security Rules v2 & Atomic Transactions

> **Objective**: Prevent open-database leaks (`allow read, write: if true;`), unbounded collection queries, and non-atomic counter/balance races in Cloud Firestore.

---

## 1. Default-Deny Security Rules v2 Blueprint

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if false; // Mandatory default deny
    }

    function isSignedIn() {
      return request.auth != null;
    }

    function isTenantMember(tenantId) {
      return isSignedIn() && request.auth.token.tenantId == tenantId;
    }

    match /tenants/{tenantId}/projects/{projectId} {
      allow read: if isTenantMember(tenantId);
      allow create: if isTenantMember(tenantId)
        && request.resource.data.keys().hasOnly(['title', 'status', 'createdAt', 'ownerId'])
        && request.resource.data.ownerId == request.auth.uid
        && request.resource.data.title is string
        && request.resource.data.title.size() > 0
        && request.resource.data.title.size() <= 200;
      allow update: if isTenantMember(tenantId)
        && request.resource.data.ownerId == resource.data.ownerId;
      allow delete: if false; // Route deletions through audited server/soft-delete flow
    }
  }
}
```

---

## 2. Schema, Transactions & Rules Ruleset
- **No Unbounded Queries**: Always paginate lists (`limit(25)` + `startAfter(lastDoc)`) and enforce `request.query.limit <= 50` in rules where appropriate.
- **Atomic `runTransaction`**: Wrap multi-document writes or counter/quota checks inside `db.runTransaction` (or `FieldValue.increment`) — never read a doc on the client and write back `count + 1`.
- **Always Delegate `firestore.rules` Edits When Specialized Tooling Applies**, and test every allow/deny path with `@firebase/rules-unit-testing`.
