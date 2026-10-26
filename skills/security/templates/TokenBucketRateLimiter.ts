/**
 * TokenBucketRateLimiter.ts - In-Memory Token Bucket Rate Limiter
 *
 * Implements defensive application-layer DDoS protection:
 * 1. Token bucket algorithm with fractional refill over time.
 * 2. Emits RFC 6585 standard headers (RateLimit-*, Retry-After).
 * 3. Returns RFC 7807 Problem Details on 429 quota exhaustion.
 * 4. Periodic sweep of inactive buckets to prevent memory leak.
 */

import type { Request, Response, NextFunction } from "express";

export interface RateLimiterOptions {
  capacity: number;       // Max tokens in the bucket (burst limit)
  refillRatePerSec: number; // Tokens added per second
  keyGenerator?: (req: Request) => string;
  errorMessage?: string;
}

interface BucketState {
  tokens: number;
  lastRefill: number;
}

export class TokenBucketStore {
  private readonly buckets = new Map<string, BucketState>();
  private readonly sweepIntervalMs = 60_000;
  private readonly idleTtlMs = 120_000;
  private sweepTimer: NodeJS.Timeout | null = null;

  constructor() {
    this.sweepTimer = setInterval(() => this.sweep(), this.sweepIntervalMs);
    if (this.sweepTimer.unref) {
      this.sweepTimer.unref(); // Do not block Node event loop from exiting
    }
  }

  public consume(
    key: string,
    capacity: number,
    refillRatePerSec: number,
    cost = 1
  ): { allowed: boolean; remaining: number; retryAfterSec: number; resetEpochSec: number } {
    const now = Date.now();
    let bucket = this.buckets.get(key);

    if (!bucket) {
      bucket = { tokens: capacity, lastRefill: now };
      this.buckets.set(key, bucket);
    } else {
      // Calculate refilled tokens based on elapsed time
      const elapsedSec = (now - bucket.lastRefill) / 1000;
      bucket.tokens = Math.min(capacity, bucket.tokens + elapsedSec * refillRatePerSec);
      bucket.lastRefill = now;
    }

    const resetEpochSec = Math.ceil(now / 1000 + (capacity - bucket.tokens) / refillRatePerSec);

    if (bucket.tokens >= cost) {
      bucket.tokens -= cost;
      return {
        allowed: true,
        remaining: Math.floor(bucket.tokens),
        retryAfterSec: 0,
        resetEpochSec
      };
    }

    const requiredTokens = cost - bucket.tokens;
    const retryAfterSec = Math.ceil(requiredTokens / refillRatePerSec);

    return {
      allowed: false,
      remaining: 0,
      retryAfterSec,
      resetEpochSec
    };
  }

  private sweep(): void {
    const cutoff = Date.now() - this.idleTtlMs;
    for (const [key, state] of this.buckets.entries()) {
      if (state.lastRefill < cutoff) {
        this.buckets.delete(key);
      }
    }
  }

  public destroy(): void {
    if (this.sweepTimer) {
      clearInterval(this.sweepTimer);
      this.sweepTimer = null;
    }
    this.buckets.clear();
  }
}

export function createRateLimiterMiddleware(options: RateLimiterOptions) {
  const store = new TokenBucketStore();
  const keyGen = options.keyGenerator || ((req) => req.ip || req.socket.remoteAddress || "anonymous");
  const msg = options.errorMessage || "Too many requests. Quota exceeded.";

  return (req: Request, res: Response, next: NextFunction): void => {
    const key = keyGen(req);
    const result = store.consume(key, options.capacity, options.refillRatePerSec, 1);

    res.setHeader("RateLimit-Limit", options.capacity.toString());
    res.setHeader("RateLimit-Remaining", result.remaining.toString());
    res.setHeader("RateLimit-Reset", result.resetEpochSec.toString());

    if (!result.allowed) {
      res.setHeader("Retry-After", result.retryAfterSec.toString());
      res.setHeader("Content-Type", "application/problem+json");
      res.status(429).json({
        type: "https://errors.skillbuilder.io/rate-limit-exceeded",
        title: "Too Many Requests",
        status: 429,
        detail: `${msg} Try again in ${result.retryAfterSec} seconds.`,
        instance: req.originalUrl || req.url,
        retryAfter: result.retryAfterSec
      });
      return;
    }

    next();
  };
}
