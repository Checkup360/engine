from fastapi.testclient import TestClient

from app.presentation.main import app

client = TestClient(app)


def test_get_version_returns_version_string() -> None:
    response = client.get("/version")
    assert response.status_code == 200
    assert "version" in response.json()
