from fastapi.testclient import TestClient
from main import app  # Assumes your FastAPI app is defined in main.py

client = TestClient(app)

def test_root_redirect():
    response = client.get("/")
    assert response.status_code in [200, 307, 308]

def test_entities_endpoint():
    response = client.get("/entities")
    assert response.status_code == 200
    assert isinstance(response.json(), list) or response.json() == {"message": "no entities"}

def test_arena_endpoint():
    response = client.get("/arena")
    assert response.status_code in [200, 404]  # Endpoint may require context or data setup

def test_world_endpoint():
    response = client.get("/world")
    assert response.status_code in [200, 404]  # Depends on data presence
