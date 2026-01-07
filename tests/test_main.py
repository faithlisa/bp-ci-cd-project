from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_readings():
    response = client.get("/readings")
    assert response.status_code == 200
