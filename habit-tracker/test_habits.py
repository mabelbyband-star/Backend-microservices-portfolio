from fastapi.testclient import TestClient
from habits import app

def test_get_habits_returns_list():
    with TestClient(app) as client:
        response = client.get("/habits")
        assert response.status_code == 200
        assert isinstance(response.json(), list)