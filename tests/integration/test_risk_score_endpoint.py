"""Integration tests for the risk score endpoint."""

from fastapi.testclient import TestClient

from app.presentation.main import app

client = TestClient(app)


def test_post_findrisc_score_returns_200_and_single_score_result() -> None:
    payload = {
        "age": 45,
        "sex": "M",
        "weight": 90.0,
        "height": 1.80,
        "waist_circumference": 96.0,
        "daily_physical_activity": True,
        "fruits_vegetables": True,
        "hypertension_medication": False,
        "previous_high_glucose": False,
        "family_diabetes": "no",
    }

    response = client.post("/risk-scores/findrisc", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["score_id"] == "findrisc"
    assert data["score_name"] == "FINDRISC"
    assert data["domain"] == "Diabetes"
    assert data["status"] == "CALCULATED"
    assert data["raw_value"] is not None
    assert "contributing_factors" in data


def test_post_missing_required_fields_returns_422() -> None:
    payload = {
        "age": 45,
        "sex": "M",
    }

    response = client.post("/risk-scores/findrisc", json=payload)

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


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


def test_post_phq9_score_returns_200_and_single_score_result() -> None:
    payload = {
        "little_interest": 1,
        "feeling_down": 1,
        "sleep_trouble": 0,
        "tired_energy": 2,
        "appetite": 0,
        "feeling_bad": 1,
        "concentration": 0,
        "psychomotor": 0,
        "self_harm_thoughts": 0,
    }

    response = client.post("/risk-scores/phq9", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["score_id"] == "phq9"
    assert data["score_name"] == "PHQ-9"
    assert data["domain"] == "Depression"
    assert data["status"] == "CALCULATED"
    assert data["raw_value"] == 5
    assert data["risk_level"] == "Mild"
    assert data["contributing_factors"]["self_harm_flag"] == 0
    assert data["attention_flags"]["self_harm_thoughts"] is False


def test_get_catalog_returns_200_and_available_scores() -> None:
    response = client.get("/risk-scores/catalog")

    assert response.status_code == 200
    catalog = response.json()
    assert isinstance(catalog, list)
    assert len(catalog) >= 2

    score_ids = [item["score_id"] for item in catalog]
    assert "findrisc" in score_ids
    assert "stop_bang" in score_ids
    assert "phq9" in score_ids

    findrisc = next(item for item in catalog if item["score_id"] == "findrisc")
    assert findrisc["score_name"] == "FINDRISC"
    assert findrisc["domain"] == "Diabetes"
    assert "age" in findrisc["required_fields"]
    assert "waist_circumference" in findrisc["required_fields"]
    assert "field_schema" in findrisc
