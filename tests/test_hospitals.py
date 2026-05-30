from fastapi.testclient import TestClient


def test_create_and_fetch_hospital(client: TestClient) -> None:
    payload = {
        "name": "Hospital Name",
        "address": "123 Main St",
        "phone": "555-1234",
        "creation_batch_id": "550e8400-e29b-41d4-a716-446655440000",
    }

    create_response = client.post("/hospitals", json=payload)

    assert create_response.status_code == 201
    created_hospital = create_response.json()
    assert created_hospital["id"] == 1
    assert created_hospital["name"] == payload["name"]
    assert created_hospital["address"] == payload["address"]
    assert created_hospital["phone"] == payload["phone"]
    assert created_hospital["creation_batch_id"] == payload["creation_batch_id"]
    assert created_hospital["active"] is True
    assert created_hospital["created_at"].endswith("Z")

    fetch_response = client.get("/hospitals/1")

    assert fetch_response.status_code == 200
    assert fetch_response.json()["name"] == payload["name"]


def test_create_hospital_generates_creation_batch_id_when_missing(client: TestClient) -> None:
    response = client.post(
        "/hospitals",
        json={
            "name": "Generated Batch Hospital",
            "address": "789 Lake Rd",
            "phone": "555-9999",
        },
    )

    assert response.status_code == 201
    generated_hospital = response.json()
    assert generated_hospital["creation_batch_id"]
    assert len(generated_hospital["creation_batch_id"]) == 36
    assert generated_hospital["active"] is True


def test_list_hospitals_with_filters(client: TestClient) -> None:
    client.post(
        "/hospitals",
        json={
            "name": "General Hospital",
            "address": "123 Main St",
            "phone": "555-1234",
            "creation_batch_id": "550e8400-e29b-41d4-a716-446655440000",
        },
    )
    client.post(
        "/hospitals",
        json={
            "name": "Active Care",
            "address": "456 High St",
            "phone": "555-5678",
            "creation_batch_id": "550e8400-e29b-41d4-a716-446655440001",
        },
    )

    all_response = client.get("/hospitals")
    active_response = client.get("/hospitals?active=true")
    batch_response = client.get("/hospitals?creation_batch_id=550e8400-e29b-41d4-a716-446655440000")

    assert all_response.status_code == 200
    assert len(all_response.json()) == 2
    assert active_response.status_code == 200
    assert len(active_response.json()) == 2
    assert batch_response.status_code == 200
    assert len(batch_response.json()) == 1
    assert batch_response.json()[0]["name"] == "General Hospital"


def test_get_missing_hospital_returns_business_error(client: TestClient) -> None:
    response = client.get("/hospitals/999")

    assert response.status_code == 404
    assert response.json()["error_code"] == "hospital_not_found"


def test_create_hospital_with_blank_name_returns_business_error(client: TestClient) -> None:
    response = client.post(
        "/hospitals",
        json={
            "name": "   ",
            "address": "123 Main St",
            "phone": "555-1234",
            "creation_batch_id": "550e8400-e29b-41d4-a716-446655440000",
        },
    )

    assert response.status_code == 400
    assert response.json()["error_code"] == "invalid_hospital_data"
