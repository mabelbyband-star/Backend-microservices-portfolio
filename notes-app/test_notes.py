from fastapi.testclient import TestClient
from notes import app

def test_get_notes_returns_list():
    with TestClient(app) as client:
        response = client.get("/notes")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

# BASIC TEST CASE 
