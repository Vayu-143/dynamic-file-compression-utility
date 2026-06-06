from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)


def test_home():

    response = client.get("/")

    assert response.status_code == 200


def test_health():

    response = client.get("/health")

    assert response.status_code == 200


def test_analytics():

    response = client.get("/analytics")

    assert response.status_code == 200