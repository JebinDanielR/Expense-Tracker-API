from fastapi.testclient import TestClient

def test_duplicate_category(client):

    client.post("/categories",
        json={
            "name":"Food"
        }
    )

    response = client.post(
        "/categories",
        json={
            "name":"Food"
        }
    )

    assert response.status_code == 409