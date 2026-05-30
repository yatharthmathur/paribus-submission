from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_healthcheck() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "Hospital Directory System"
