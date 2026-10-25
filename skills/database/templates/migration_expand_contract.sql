-- ==============================================================================
-- Zero-Downtime Expand-and-Contract Migration Template (PostgreSQL)
-- Step 1: Expand (Add new column without locking)
-- ==============================================================================

SET lock_timeout = '3s';
SET statement_timeout = '30s';

-- 1. Add new column with nullable constraint
ALTER TABLE users ADD COLUMN phone_number_e164 VARCHAR(20) NULL;

-- 2. Create index concurrently (outside transaction block)
-- Note: In PostgreSQL, CONCURRENTLY cannot run inside a multi-statement transaction
-- Run separately:
-- CREATE INDEX CONCURRENTLY idx_users_phone ON users(phone_number_e164) WHERE phone_number_e164 IS NOT NULL;

-- ==============================================================================
-- Step 2: Backfill (Run via application batch job, 500 rows at a time)
-- UPDATE users SET phone_number_e164 = normalize_phone(phone_raw) WHERE id IN (...)
-- ==============================================================================

-- ==============================================================================
-- Step 3: Contract (Drop old deprecated column in a subsequent deployment)
-- ALTER TABLE users DROP COLUMN phone_raw;
-- ==============================================================================
