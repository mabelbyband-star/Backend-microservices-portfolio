from fastapi.testclient import TestClient
from notes import app

client = TestClient(app)

def test_get_notes_returns_list():
    response = client.get("/notes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# BASIC TEST CASE 
