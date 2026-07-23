from tests.conftest import client

def test_duplicate_category():

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