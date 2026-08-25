from fastapi.testclient import TestClient
from bank import app

def test_register_and_check_balance():
    with TestClient(app) as client:
        response = client.post("/accounts/register", json={
            "name": "Test",
            "last_name": "User",
            "email": "test_user_for_ci@example.com",
            "password": "TestPass123",
            "opening_balance": 100
        })
        assert response.status_code == 200
        account_id = response.json()["account_id"]

        balance_response = client.get(f"/accounts/{account_id}/balance")
        assert balance_response.status_code == 200
        assert balance_response.json()["balance"] == 100.0