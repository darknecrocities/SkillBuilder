# Authentication & Access Control (AuthN / AuthZ)

Production security patterns for identity, session tokens, and permissions.

---

## 1. Token Architecture: Access vs Refresh Tokens
- **Access Token**: Short-lived (15 minutes). Sent in `Authorization: Bearer <token>`. Contains user ID, tenant ID, and roles.
- **Refresh Token**: Long-lived (7–30 days). Stored in an `HttpOnly`, `Secure`, `SameSite=Strict` cookie.
- **Refresh Token Rotation**: Invalidate old refresh token immediately upon issuance of a new pair. If a revoked token is presented, invalidate all sessions for that user (compromise detection).

---

## 2. Role-Based & Attribute-Based Access Control (RBAC / ABAC)

```typescript
export function requireRole(allowedRoles: string[]) {
  return (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
    if (!req.user || !allowedRoles.includes(req.user.role)) {
      return res.status(403).json({
        type: "https://api.example.com/errors/forbidden",
        title: "Forbidden",
        status: 403,
        detail: "User lacks required role to perform this action.",
      });
    }
    next();
  };
}
```
