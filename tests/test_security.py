from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint_needs_no_auth():
    response = client.get("/health")
    assert response.status_code == 200


def test_protected_endpoint_rejects_missing_api_key():
    response = client.get("/model/eval-report")
    assert response.status_code == 401


def test_protected_endpoint_rejects_wrong_api_key():
    response = client.get("/model/eval-report", headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 401
