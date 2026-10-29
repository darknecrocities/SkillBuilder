# Supabase PostgreSQL Row Level Security (RLS)

Every table exposed to Supabase client queries must enable Row Level Security (RLS) with explicit policies.

---

## 1. Enabling RLS & Tenant Scoping

```sql
-- 1. Enable RLS
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- 2. Scoped SELECT Policy
CREATE POLICY "Users can read own documents"
ON documents FOR SELECT
USING (auth.uid() = user_id);

-- 3. Scoped INSERT Policy
CREATE POLICY "Users can insert own documents"
ON documents FOR INSERT
WITH CHECK (auth.uid() = user_id);
```

---

## 2. Service Role & Bypass Protection

- Client queries using `anon` or `authenticated` keys cannot bypass RLS.
- Use `service_role` keys exclusively in serverless Edge Functions or backend microservices. Never leak `service_role` keys to client bundles.
