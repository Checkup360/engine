"""Unit tests for SCORE2Calculator."""

import pytest

from app.domain.calculators.score2 import SCORE2Calculator
from app.domain.entities.score2_data import Score2Data
from app.domain.value_objects.score_result import CalculationStatus


def _base_data(**overrides: object) -> Score2Data:
    values: dict[str, object] = {
        "age": 60,
        "sex": "M",
        "smoker": False,
        "systolic_blood_pressure": 120.0,
        "total_cholesterol": 6.0,
        "hdl_cholesterol": 1.3,
        "risk_region": "moderate",
    }
    values.update(overrides)
    return Score2Data(**values)


def test_score2_not_calculable_if_required_fields_missing() -> None:
    calculator = SCORE2Calculator()

    # Empty data
    result = calculator.calculate(Score2Data())
    assert result.status == CalculationStatus.NOT_CALCULABLE
    assert result.score_id == "score2"

    # Missing smoker
    result = calculator.calculate(_base_data(smoker=None))
    assert result.status == CalculationStatus.NOT_CALCULABLE

    # Invalid sex
    result = calculator.calculate(_base_data(sex="other"))
    assert result.status == CalculationStatus.NOT_CALCULABLE

    # Invalid region
    result = calculator.calculate(_base_data(risk_region="antarctica"))
    assert result.status == CalculationStatus.NOT_CALCULABLE


def test_score2_calculates_male_baseline_moderate_region() -> None:
    calculator = SCORE2Calculator()
    result = calculator.calculate(_base_data(sex="M", risk_region="moderate"))

    assert result.status == CalculationStatus.CALCULATED
    assert result.score_id == "score2"
    assert result.score_name == "SCORE2"
    assert result.domain == "Cardiovascular"
    assert result.raw_value == 6.3
    assert result.risk_value == 21.0
    assert result.risk_level == "Moderate risk"
    assert result.attention_flags["high_cardiovascular_risk"] is False
    assert result.attention_flags["smoker"] is False
    assert result.attention_flags["elevated_blood_pressure"] is False


def test_score2_calculates_female_baseline_moderate_region() -> None:
    calculator = SCORE2Calculator()
    result = calculator.calculate(_base_data(sex="F", risk_region="moderate"))

    assert result.status == CalculationStatus.CALCULATED
    assert result.raw_value == 3.9
    assert result.risk_level == "Low risk"
    assert result.attention_flags["high_cardiovascular_risk"] is False


def test_score2_converts_mg_dl_to_mmol_l_transparently() -> None:
    calculator = SCORE2Calculator()

    # 6.0 mmol/L * 38.67 ~ 232.02 mg/dL; 1.3 mmol/L * 38.67 ~ 50.27 mg/dL
    result_mgdl = calculator.calculate(
        _base_data(
            sex="M",
            total_cholesterol=232.02,
            hdl_cholesterol=50.27,
            risk_region="moderate",
        )
    )

    result_mmol = calculator.calculate(
        _base_data(
            sex="M",
            total_cholesterol=6.0,
            hdl_cholesterol=1.3,
            risk_region="moderate",
        )
    )

    assert result_mgdl.status == CalculationStatus.CALCULATED
    assert result_mgdl.raw_value == pytest.approx(result_mmol.raw_value, abs=0.1)


def test_score2_high_risk_and_attention_flags() -> None:
    calculator = SCORE2Calculator()
    result = calculator.calculate(
        _base_data(
            age=68,
            sex="M",
            smoker=True,
            systolic_blood_pressure=160.0,
            total_cholesterol=7.5,
            hdl_cholesterol=0.9,
            risk_region="high",
        )
    )

    assert result.status == CalculationStatus.CALCULATED
    assert result.raw_value > 20.0
    assert result.risk_level == "Very high risk"
    assert result.attention_flags["high_cardiovascular_risk"] is True
    assert result.attention_flags["smoker"] is True
    assert result.attention_flags["elevated_blood_pressure"] is True


def test_score2_supports_all_european_risk_regions() -> None:
    calculator = SCORE2Calculator()
    regions = ["low", "moderate", "high", "very_high"]
    results = [
        calculator.calculate(_base_data(risk_region=reg)).raw_value for reg in regions
    ]

    # Risk should strictly increase from low to moderate to high to very_high
    for i in range(len(results) - 1):
        assert results[i] < results[i + 1]
