from fastapi.testclient import TestClient


def test_root_healthcheck(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "Hospital Directory System"
