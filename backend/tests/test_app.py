from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "backend",
        "version": "v1.0.0",
    }


def test_version() -> None:
    response = client.get("/api/version")
    assert response.status_code == 200
    assert response.json() == {"version": "v1.0.0"}


def test_message() -> None:
    response = client.get("/api/message")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello from CI/CD Observability Demo",
        "version": "v1.0.0",
    }


def test_items() -> None:
    response = client.get("/api/items")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Continuous Integration"},
        {"id": 2, "name": "Continuous Delivery"},
        {"id": 3, "name": "Cloud Observability"},
    ]


def test_error() -> None:
    response = client.get("/api/error", headers={"x-request-id": "demo-test-id"})
    assert response.status_code == 500
    assert response.json() == {"error": "Simulated internal server error"}
    assert response.headers["x-request-id"] == "demo-test-id"


def test_metrics() -> None:
    client.get("/api/health")
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text
    assert "http_request_duration_seconds" in response.text
    assert "http_errors_total" in response.text
    assert 'app_info{service="backend",version="v1.0.0"}' in response.text
