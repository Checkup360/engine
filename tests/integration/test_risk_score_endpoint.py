"""Integration tests for the risk score endpoint."""

from fastapi.testclient import TestClient

from app.presentation.main import app

client = TestClient(app)


def test_post_findrisc_score_returns_200_and_single_score_result() -> None:
    payload = {
        "age": 45,
        "sex": "M",
        "weight": 90,
    }

    response = client.post("/risk-scores/findrisc", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["score_id"] == "findrisc"
    assert data["score_name"] == "FINDRISC"
    assert data["domain"] == "Diabetes"
    assert data["status"] == "NOT_CALCULABLE"
    assert "contributing_factors" in data


def test_post_stop_bang_score_returns_200_and_single_score_result() -> None:
    payload = {
        "age": 55,
        "sex": "M",
        "weight": 95,
        "height": 1.75,
        "snoring": True,
        "tired": True,
        "observed_apnea": False,
        "hypertension_medication": True,
        "neck_circumference": 43,
    }

    response = client.post("/risk-scores/stop_bang", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["score_id"] == "stop_bang"
    assert data["score_name"] == "STOP-BANG"
    assert data["domain"] == "Sleep Apnea"
    assert data["status"] == "CALCULATED"
    assert data["raw_value"] is not None
    assert data["risk_level"] is not None
    assert "contributing_factors" in data


def test_post_unknown_score_returns_404() -> None:
    payload = {
        "age": 45,
        "sex": "M",
    }

    response = client.post("/risk-scores/unknown_score", json=payload)

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "unknown_score" in data["detail"]


def test_post_invalid_payload_types_returns_422() -> None:
    payload = {
        "age": "not_an_integer",
    }

    response = client.post("/risk-scores/findrisc", json=payload)

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
