from tests.conftest import client

def test_create_expense(category):

    response = client.post("/expenses",
        json={
            "amount":100,
            "description":"Coffee",
            "spent_on":"2026-03-10",
            "category_id":category["id"]
        }
    )

    assert response.status_code == 201
    data=response.json()
    assert data["amount"] == 100

def test_negative_amount(category):

    response = client.post("/expenses",
        json={
            "amount":-100,
            "description":"Invalid",
            "spent_on":"2026-03-10",
            "category_id":category["id"]
        }
    )

    assert response.status_code == 422

def test_expense_not_found():

    response = client.get("/expenses/999")

    assert response.status_code == 404



