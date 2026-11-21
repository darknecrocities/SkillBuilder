# Supabase PostgreSQL Row-Level Security (RLS) & Auth Manual

> **Objective**: Guarantee tenant and user data isolation directly in PostgreSQL so even exposed anon keys or buggy client queries cannot leak unauthorized rows.

---

## 1. Mandatory RLS Pattern on Every Public Table

Never leave RLS disabled on tables inside the `public` schema exposed to PostgREST:

```sql
ALTER TABLE public.projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.projects FORCE ROW LEVEL SECURITY;

-- Performance index for RLS predicate columns
CREATE INDEX IF NOT EXISTS idx_projects_owner_id ON public.projects (owner_id);

CREATE POLICY "projects_select_own"
  ON public.projects FOR SELECT
  TO authenticated
  USING ((SELECT auth.uid()) = owner_id);

CREATE POLICY "projects_insert_own"
  ON public.projects FOR INSERT
  TO authenticated
  WITH CHECK ((SELECT auth.uid()) = owner_id);

CREATE POLICY "projects_update_own"
  ON public.projects FOR UPDATE
  TO authenticated
  USING ((SELECT auth.uid()) = owner_id)
  WITH CHECK ((SELECT auth.uid()) = owner_id);
```

### Critical RLS Performance & Security Rules
1. **Wrap `auth.uid()` in `(SELECT auth.uid())`**: Enables PostgreSQL initPlan caching once per statement instead of re-evaluating per row (`10–50x` faster on large scans).
2. **Always Pair `USING` + `WITH CHECK` on `UPDATE`**: Without `WITH CHECK`, an attacker could update `owner_id` to hijack or transfer rows into another tenant!
3. **Never Expose `service_role` Key in Client Bundles**: Keep `SUPABASE_SERVICE_ROLE_KEY` strictly on trusted servers/Edge Functions.
4. **Pre-Migration Backups**: Run `manage_deduplicated_backup.py` before altering RLS policies or dropping columns.
