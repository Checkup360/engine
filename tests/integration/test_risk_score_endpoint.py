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

    response = client.post("/risk-scores", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert "scores" in data
    scores = data["scores"]
    assert len(scores) == 2

    expected_score_ids = {
        "findrisc",
        "stop_bang",
    }

    actual_score_ids = {s["score_id"] for s in scores}
    assert actual_score_ids == expected_score_ids

    for score in scores:
        assert score["status"] == "NOT_CALCULABLE"


def test_post_risk_scores_with_query_param_returns_only_requested() -> None:
    payload = {
        "age": 45,
        "sex": "M",
        "weight": 90,
    }

    response = client.post("/risk-scores?target_scores=findrisc", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "scores" in data
    assert len(data["scores"]) == 1
    assert data["scores"][0]["score_id"] == "findrisc"
