from datetime import datetime

from apps.health_service.routes.health_routes import health_check


def test_health_check_returns_ok_status():
    payload = health_check()

    assert payload["status"] == "ok"
    assert datetime.fromisoformat(payload["timestamp"])
