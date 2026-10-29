# Firebase Auth & Admin SDK Production Standards

---

## 1. Firebase Auth Client Integration

- Store session tokens securely (use httpOnly session cookies for Server-Side Rendering rather than raw local storage).
- Enforce Multi-Factor Authentication (MFA) on administrative routes.
- Verify ID tokens server-side on every protected API call using `admin.auth().verifyIdToken(idToken)`.

---

## 2. Admin SDK Backend Execution

```typescript
import * as admin from 'firebase-admin';

if (!admin.apps.length) {
  admin.initializeApp({
    credential: admin.credential.applicationDefault()
  });
}

export const db = admin.firestore();
export const auth = admin.auth();
```

### Security Rules:
- Never bundle the Firebase Admin SDK or service account private keys into client-side web bundles.
- Use Application Default Credentials (ADC) when deploying to Cloud Run or Google Kubernetes Engine.
