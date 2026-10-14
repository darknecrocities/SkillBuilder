"""
resilient_http_client.py - Production-ready HTTP client wrapper.

Features:
- Explicit socket and read timeouts
- In-memory caching with TTL and invalidation on mutations
- Bounded exponential backoff with full jitter
- Idempotency guard (never blindly retries unsafe POST requests)
"""

from __future__ import annotations

import json
import random
import time
import urllib.error
import urllib.request
from typing import Any, Dict, Optional, Tuple


class ResilientHttpClient:
    """Zero-dependency resilient HTTP client using standard library urllib."""

    def __init__(
        self,
        timeout_seconds: float = 5.0,
        max_retries: int = 3,
        base_backoff_seconds: float = 0.3,
        max_backoff_seconds: float = 5.0,
        enable_cache: bool = True,
        default_ttl_seconds: float = 60.0,
    ) -> None:
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self.base_backoff_seconds = base_backoff_seconds
        self.max_backoff_seconds = max_backoff_seconds
        self.enable_cache = enable_cache
        self.default_ttl_seconds = default_ttl_seconds

        # Cache key -> (data, expires_at_timestamp)
        self._cache: Dict[str, Tuple[Any, float]] = {}

    def request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Dict[str, Any]] = None,
        custom_ttl_seconds: Optional[float] = None,
    ) -> Any:
        """Send an HTTP request with timeout, caching, and retry protections."""
        method_upper = method.upper()
        is_idempotent = method_upper in {"GET", "HEAD", "PUT", "DELETE", "OPTIONS"}
        cache_key = f"{method_upper}:{url}"

        # 1. Check cache for GET requests
        if self.enable_cache and method_upper == "GET":
            if cache_key in self._cache:
                cached_data, expires_at = self._cache[cache_key]
                if expires_at > time.time():
                    return cached_data
                del self._cache[cache_key]

        # 2. Encode payload if provided
        encoded_data = json.dumps(data).encode("utf-8") if data is not None else None
        req_headers = {"Accept": "application/json"}
        if data is not None:
            req_headers["Content-Type"] = "application/json"
        if headers:
            req_headers.update(headers)

        # 3. Execute with bounded retries
        max_attempts = self.max_retries if is_idempotent else 0
        attempt = 0
        last_error: Optional[Exception] = None

        while attempt <= max_attempts:
            try:
                req = urllib.request.Request(
                    url=url,
                    data=encoded_data,
                    headers=req_headers,
                    method=method_upper,
                )
                with urllib.request.urlopen(req, timeout=self.timeout_seconds) as response:
                    payload = response.read().decode("utf-8")
                    result = json.loads(payload) if payload else {}

                # Cache successful GET responses
                if self.enable_cache and method_upper == "GET":
                    ttl = custom_ttl_seconds or self.default_ttl_seconds
                    self._cache[cache_key] = (result, time.time() + ttl)

                # Invalidate cache on state mutations
                if method_upper in {"POST", "PUT", "PATCH", "DELETE"}:
                    self.invalidate_url(url)

                return result

            except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as err:
                last_error = err
                attempt += 1

                if attempt > max_attempts:
                    break

                # Exponential backoff with full random jitter
                backoff = min(
                    self.max_backoff_seconds,
                    self.base_backoff_seconds * (2 ** attempt),
                )
                jittered_backoff = random.uniform(0, backoff)
                time.sleep(jittered_backoff)

        raise RuntimeError(f"Request failed after {attempt} attempts: {last_error}")

    def invalidate_url(self, url: str) -> None:
        """Purge cached responses matching url."""
        keys_to_delete = [k for k in self._cache if url in k]
        for k in keys_to_delete:
            del self._cache[k]

    def clear_cache(self) -> None:
        """Clear entire cache."""
        self._cache.clear()
