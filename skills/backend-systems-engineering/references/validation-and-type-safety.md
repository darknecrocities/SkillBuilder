# Validation & Type Safety at Runtime

Techniques for enforcing runtime boundaries with Zod (TypeScript) and Pydantic v2 (Python).

---

## 1. Zod Boundary Schema (TypeScript)

```typescript
import { z } from "zod";

export const CreateUserSchema = z.object({
  email: z.string().email().toLowerCase().trim(),
  password: z.string().min(8).max(100),
  role: z.enum(["admin", "member", "viewer"]).default("member"),
  metadata: z.record(z.string()).optional(),
});

export type CreateUserInput = z.infer<typeof CreateUserSchema>;
```

---

## 2. Pydantic v2 Boundary Schema (Python)

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal

class CreateUserSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    role: Literal["admin", "member", "viewer"] = "member"
    metadata: Optional[dict[str, str]] = None

    class Config:
        str_strip_whitespace = True
```

- Always strip whitespace on user text inputs.
- Convert emails to lowercase to prevent duplicate account creation bugs.
