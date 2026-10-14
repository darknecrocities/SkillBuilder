/**
 * resilient_http_client.ts
 *
 * Production-ready HTTP client wrapper with:
 * - Explicit connection & read timeouts (AbortController)
 * - In-memory cache with TTL and deliberate cache invalidation
 * - Bounded retries with exponential backoff and full random jitter
 * - Idempotency protection (never blindly retries unsafe POST requests)
 */

export interface HttpClientOptions {
  timeoutMs?: number;
  maxRetries?: number;
  baseBackoffMs?: number;
  maxBackoffMs?: number;
  enableCache?: boolean;
  defaultTtlMs?: number;
}

export interface CacheEntry<T> {
  data: T;
  expiresAt: number;
}

export class ResilientHttpClient {
  private readonly timeoutMs: number;
  private readonly maxRetries: number;
  private readonly baseBackoffMs: number;
  private readonly maxBackoffMs: number;
  private readonly enableCache: boolean;
  private readonly defaultTtlMs: number;

  private readonly cache = new Map<string, CacheEntry<unknown>>();

  constructor(options: HttpClientOptions = {}) {
    this.timeoutMs = options.timeoutMs ?? 5000;
    this.maxRetries = options.maxRetries ?? 3;
    this.baseBackoffMs = options.baseBackoffMs ?? 300;
    this.maxBackoffMs = options.maxBackoffMs ?? 5000;
    this.enableCache = options.enableCache ?? true;
    this.defaultTtlMs = options.defaultTtlMs ?? 60_000; // 1 minute default
  }

  /**
   * Send a request with timeout, caching, and retry protection.
   */
  async request<T>(
    url: string,
    init: RequestInit = {},
    customTtlMs?: number
  ): Promise<T> {
    const method = (init.method ?? "GET").toUpperCase();
    const isIdempotent = ["GET", "HEAD", "PUT", "DELETE", "OPTIONS"].includes(method);
    const cacheKey = `${method}:${url}`;

    // 1. Check cache for GET requests
    if (this.enableCache && method === "GET") {
      const cached = this.cache.get(cacheKey);
      if (cached && cached.expiresAt > Date.now()) {
        return cached.data as T;
      }
      this.cache.delete(cacheKey);
    }

    // 2. Perform request with bounded retries
    let attempt = 0;
    let lastError: Error | null = null;

    while (attempt <= (isIdempotent ? this.maxRetries : 0)) {
      try {
        const data = await this.executeWithTimeout<T>(url, init);

        // Populate cache for successful GET responses
        if (this.enableCache && method === "GET") {
          const ttl = customTtlMs ?? this.defaultTtlMs;
          this.cache.set(cacheKey, { data, expiresAt: Date.now() + ttl });
        }

        // Invalidate cache on state-changing mutations
        if (["POST", "PUT", "PATCH", "DELETE"].includes(method)) {
          this.invalidateUrl(url);
        }

        return data;
      } catch (err: unknown) {
        lastError = err instanceof Error ? err : new Error(String(err));
        attempt++;

        if (attempt > (isIdempotent ? this.maxRetries : 0)) {
          break;
        }

        // Calculate exponential backoff with full jitter
        const backoff = Math.min(
          this.maxBackoffMs,
          this.baseBackoffMs * Math.pow(2, attempt)
        );
        const jitteredBackoff = Math.random() * backoff;
        await new Promise((resolve) => setTimeout(resolve, jitteredBackoff));
      }
    }

    throw lastError ?? new Error(`Request failed after ${attempt} attempts`);
  }

  private async executeWithTimeout<T>(url: string, init: RequestInit): Promise<T> {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeoutMs);

    try {
      const response = await fetch(url, {
        ...init,
        signal: controller.signal,
      });

      if (!response.ok) {
        throw new Error(`HTTP Error ${response.status}: ${response.statusText}`);
      }

      return (await response.json()) as T;
    } finally {
      clearTimeout(timer);
    }
  }

  /** Invalidate specific cached key or pattern */
  invalidateUrl(url: string): void {
    for (const key of this.cache.keys()) {
      if (key.includes(url)) {
        this.cache.delete(key);
      }
    }
  }

  clearCache(): void {
    this.cache.clear();
  }
}
