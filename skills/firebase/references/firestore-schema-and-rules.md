# Cloud Firestore Schema Design & Security Rules

---

## 1. Firestore Data Modeling Guidelines

- **Subcollections vs Root Collections**: Use subcollections (`users/{userId}/orders/{orderId}`) when access is hierarchically scoped to an owner.
- **Denormalization**: Store frequently displayed read data directly on the parent document (e.g., `userName`, `avatarUrl`) to prevent multiple reads.
- **Index Optimization**: Explicitly define composite indexes in `firestore.indexes.json` for queries with inequality filters and sorting.

---

## 2. Hardened Security Rules (`firestore.rules`)

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

    match /users/{userId} {
      allow read: if isAuthenticated();
      allow write: if isOwner(userId);

      match /private/{docId} {
        allow read, write: if isOwner(userId);
      }
    }
  }
}
```
