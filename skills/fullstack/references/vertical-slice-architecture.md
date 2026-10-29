# Vertical Slice Architecture for Fullstack Features

Vertical slices package all tiers of a feature together (presentation, business logic, persistence) rather than segregating by technical layer.

---

## 1. Directory Organization

```text
features/user-registration/
├── UserRegistrationForm.tsx    # Leaf presentation
├── register-user.action.ts     # Zod validation & transaction logic
├── user-repository.ts          # Database SQL / Prisma queries
├── user-schema.ts              # Domain types
└── user-registration.test.ts   # Integration test
```

### Benefits:
- High cohesion: Modifying the registration flow affects only one directory.
- Easy refactoring and deletion: Removing a feature requires deleting one folder with zero orphaned layers.
- Strict anti-mock integration: Every slice tests the complete journey from user input to persisted database rows.
