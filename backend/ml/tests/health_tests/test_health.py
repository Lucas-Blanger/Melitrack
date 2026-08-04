import pytest

from app.routes.health import health


@pytest.mark.anyio
async def test_health_returns_ok():
    assert await health() == {"status": "ok", "service": "ml"}
