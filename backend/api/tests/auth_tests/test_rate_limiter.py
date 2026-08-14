from core.rate_limiter import InMemoryRateLimiter


def test_rate_limiter_allows_requests_inside_limit():
    limiter = InMemoryRateLimiter()

    first = limiter.check("client-a", limit=2, window_seconds=60)
    second = limiter.check("client-a", limit=2, window_seconds=60)

    assert first.allowed is True
    assert first.remaining == 1
    assert second.allowed is True
    assert second.remaining == 0


def test_rate_limiter_blocks_requests_over_limit():
    limiter = InMemoryRateLimiter()

    limiter.check("client-a", limit=1, window_seconds=60)
    blocked = limiter.check("client-a", limit=1, window_seconds=60)

    assert blocked.allowed is False
    assert blocked.remaining == 0
    assert blocked.retry_after > 0
