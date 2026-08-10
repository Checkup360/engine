"""Integration tests for the risk score endpoint."""

from fastapi.testclient import TestClient

from app.presentation.main import app

client = TestClient(app)


def test_post_risk_score_returns_200_and_all_stubs_not_calculable() -> None:
    payload = {
        "age": 45,
        "sex": "M",
        "weight": 90,
    }

    response = client.post("/api/v1/risk-score", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert "scores" in data
    scores = data["scores"]
    assert len(scores) == 1

    expected_score_ids = {
        "findrisc",
    }

    actual_score_ids = {s["score_id"] for s in scores}
    assert actual_score_ids == expected_score_ids

    for score in scores:
        assert score["status"] == "NOT_CALCULABLE"
