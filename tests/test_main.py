from fastapi.testclient import TestClient
from app.main import app

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200


def test_unexpected_error_returns_500(client):
    @client.app.get("/test-error")
    def trigger_error():
        raise RuntimeError("Test error")

    with TestClient(app, raise_server_exceptions=False) as test_client:
       response = test_client.get("/test-error")

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}
