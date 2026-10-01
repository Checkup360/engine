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
    assert 0.0 <= data["health_index"] <= 100.0
    assert "risk_value" not in data
    assert "normalized_value" not in data
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
    assert data["risk_level"] == "Mild risk"
    assert data["contributing_factors"]["self_harm_flag"] == 0
    assert data["attention_flags"]["self_harm_thoughts"] is False


def test_post_metabolic_syndrome_returns_200_and_criteria_result() -> None:
    payload = {
        "sex": "M",
        "waist_circumference": 105.0,
        "triglycerides": 180.0,
        "hdl_cholesterol": 38.0,
        "systolic_blood_pressure": 135.0,
        "diastolic_blood_pressure": 85.0,
        "hypertension_medication": False,
        "fasting_glucose": 95.0,
        "glucose_lowering_medication": False,
    }

    response = client.post("/risk-scores/metabolic_syndrome", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["score_id"] == "metabolic_syndrome"
    assert data["score_name"] == "Metabolic Syndrome"
    assert data["raw_value"] == 4
    assert data["attention_flags"]["metabolic_syndrome"] is True


def test_post_eoss_returns_200_and_highest_stage() -> None:
    response = client.post(
        "/risk-scores/eoss",
        json={
            "physical_health_stage": 1,
            "mental_health_stage": 2,
            "functional_stage": 3,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["score_id"] == "eoss"
    assert data["score_name"] == "EOSS"
    assert data["raw_value"] == 3
    assert data["risk_level"] == "High risk"


def test_post_score2_returns_200_and_cardiovascular_result() -> None:
    payload = {
        "age": 60,
        "sex": "M",
        "smoker": False,
        "systolic_blood_pressure": 120.0,
        "total_cholesterol": 6.0,
        "hdl_cholesterol": 1.3,
        "risk_region": "moderate",
    }

    response = client.post("/risk-scores/score2", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["score_id"] == "score2"
    assert data["score_name"] == "SCORE2"
    assert data["domain"] == "Cardiovascular"
    assert data["status"] == "CALCULATED"
    assert data["raw_value"] == 6.3
    assert data["risk_level"] == "Moderate risk"
    assert data["attention_flags"]["high_cardiovascular_risk"] is False


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
    assert "score2" in score_ids

    findrisc = next(item for item in catalog if item["score_id"] == "findrisc")
    assert findrisc["score_name"] == "FINDRISC"
    assert findrisc["domain"] == "Diabetes"
    assert "age" in findrisc["required_fields"]
    assert "waist_circumference" in findrisc["required_fields"]
    assert "field_schema" in findrisc


def test_post_score_with_lowercase_sex_returns_200() -> None:
    payload = {
        "age": 45,
        "sex": "m",
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
    assert response.json()["status"] == "CALCULATED"
