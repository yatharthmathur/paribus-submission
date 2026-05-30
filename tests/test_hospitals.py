from uuid import UUID

from fastapi.testclient import TestClient


def test_create_and_fetch_hospital(client: TestClient) -> None:
    payload = {
        "name": "Hospital Name",
        "address": "123 Main St",
        "phone": "555-1234",
    }

    create_response = client.post("/hospitals", json=payload)

    assert create_response.status_code == 201
    created_hospital = create_response.json()
    assert created_hospital["id"] == 1
    assert created_hospital["name"] == payload["name"]
    assert created_hospital["address"] == payload["address"]
    assert created_hospital["phone"] == payload["phone"]
    assert created_hospital["creation_batch_id"]
    assert UUID(created_hospital["creation_batch_id"])
    assert created_hospital["active"] is True
    assert created_hospital["created_at"].endswith("Z")

    fetch_response = client.get("/hospitals/1")

    assert fetch_response.status_code == 200
    assert fetch_response.json()["name"] == payload["name"]
    assert fetch_response.json()["creation_batch_id"] == created_hospital["creation_batch_id"]


def test_create_hospital_uses_provided_creation_batch_id(client: TestClient) -> None:
    payload = {
        "name": "Hospital Name",
        "address": "123 Main St",
        "phone": "555-1234",
        "creation_batch_id": "550e8400-e29b-41d4-a716-446655440000",
    }

    response = client.post("/hospitals", json=payload)

    assert response.status_code == 201
    assert response.json()["creation_batch_id"] == payload["creation_batch_id"]


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


def test_list_hospitals_and_get_hospitals_by_batch_id(client: TestClient) -> None:
    first_batch_id = "550e8400-e29b-41d4-a716-446655440000"
    second_batch_id = "550e8400-e29b-41d4-a716-446655440001"

    client.post(
        "/hospitals",
        json={
            "name": "General Hospital",
            "address": "123 Main St",
            "phone": "555-1234",
            "creation_batch_id": first_batch_id,
        },
    )
    client.post(
        "/hospitals",
        json={
            "name": "Active Care",
            "address": "456 High St",
            "phone": "555-5678",
            "creation_batch_id": second_batch_id,
        },
    )

    all_response = client.get("/hospitals")
    batch_response = client.get(f"/hospitals/batch/{first_batch_id}")

    assert all_response.status_code == 200
    assert len(all_response.json()) == 2
    assert batch_response.status_code == 200
    assert len(batch_response.json()) == 1
    assert batch_response.json()[0]["name"] == "General Hospital"
    assert batch_response.json()[0]["creation_batch_id"] == first_batch_id


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
        },
    )

    assert response.status_code == 400
    assert response.json()["error_code"] == "invalid_hospital_data"
