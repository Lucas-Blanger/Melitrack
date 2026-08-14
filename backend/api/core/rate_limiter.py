from __future__ import annotations

import time
from dataclasses import dataclass
from threading import Lock
from typing import Callable

from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response


@dataclass
class RateLimitResult:
    allowed: bool
    retry_after: int
    remaining: int
    reset_after: int


@dataclass
class _Bucket:
    count: int
    reset_at: float


class InMemoryRateLimiter:
    def __init__(self) -> None:
        self._buckets: dict[str, _Bucket] = {}
        self._lock = Lock()

    def check(self, key: str, limit: int, window_seconds: int) -> RateLimitResult:
        now = time.monotonic()

        with self._lock:
            self._cleanup(now)

            bucket = self._buckets.get(key)
            if bucket is None or now >= bucket.reset_at:
                bucket = _Bucket(count=0, reset_at=now + window_seconds)
                self._buckets[key] = bucket

            reset_after = max(1, int(bucket.reset_at - now))

            if bucket.count >= limit:
                return RateLimitResult(
                    allowed=False,
                    retry_after=reset_after,
                    remaining=0,
                    reset_after=reset_after,
                )

            bucket.count += 1
            return RateLimitResult(
                allowed=True,
                retry_after=0,
                remaining=max(0, limit - bucket.count),
                reset_after=reset_after,
            )

    def _cleanup(self, now: float) -> None:
        expired_keys = [
            key for key, bucket in self._buckets.items() if now >= bucket.reset_at
        ]

        for key in expired_keys:
            del self._buckets[key]


rate_limiter = InMemoryRateLimiter()


def get_client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",", 1)[0].strip()

    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip

    if request.client:
        return request.client.host

    return "unknown"


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        *,
        limiter: InMemoryRateLimiter,
        limit: int,
        window_seconds: int,
        enabled: bool = True,
    ) -> None:
        super().__init__(app)
        self.limiter = limiter
        self.limit = limit
        self.window_seconds = window_seconds
        self.enabled = enabled

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if not self.enabled or request.method == "OPTIONS":
            return await call_next(request)

        key = f"global:{get_client_ip(request)}"
        result = self.limiter.check(key, self.limit, self.window_seconds)

        if not result.allowed:
            return _rate_limit_response(result)

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.limit)
        response.headers["X-RateLimit-Remaining"] = str(result.remaining)
        response.headers["X-RateLimit-Reset"] = str(result.reset_after)
        return response


def rate_limit(
    *,
    name: str,
    limit: int,
    window_seconds: int,
    enabled: bool = True,
):
    async def dependency(request: Request) -> None:
        if not enabled:
            return

        key = f"{name}:{get_client_ip(request)}"
        result = rate_limiter.check(key, limit, window_seconds)

        if result.allowed:
            return

        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Try again later.",
            headers={
                "Retry-After": str(result.retry_after),
                "X-RateLimit-Limit": str(limit),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(result.reset_after),
            },
        )

    return dependency


def _rate_limit_response(result: RateLimitResult) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": "Too many requests. Try again later."},
        headers={
            "Retry-After": str(result.retry_after),
            "X-RateLimit-Remaining": "0",
            "X-RateLimit-Reset": str(result.reset_after),
        },
    )
