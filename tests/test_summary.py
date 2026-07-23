from fastapi.testclient import TestClient
from tests.conftest import client

def test_summary():

    response = client.get("/summary?month=2026-03")

    assert response.status_code == 200
    data=response.json()

    assert "total_spend" in data
    assert "breakdown" in data