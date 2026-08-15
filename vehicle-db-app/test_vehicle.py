from fastapi.testclient import TestClient
from vehicle import app

def test_get_vehicles_returns_dict_with_list():
    with TestClient(app) as client:
        response = client.get("/vehicles")
        assert response.status_code == 200
        assert "vehicles" in response.json()
        assert isinstance(response.json()["vehicles"], list)