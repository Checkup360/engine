"""Unit tests for MetabolicSyndromeCalculator."""

from app.domain.calculators.metabolic_syndrome import MetabolicSyndromeCalculator
from app.domain.entities.metabolic_syndrome_data import MetabolicSyndromeData
from app.domain.value_objects.score_result import CalculationStatus


def _base_data(**overrides: object) -> MetabolicSyndromeData:
    values: dict[str, object] = {
        "sex": "M",
        "waist_circumference": 90.0,
        "triglycerides": 100.0,
        "hdl_cholesterol": 50.0,
        "systolic_blood_pressure": 120.0,
        "diastolic_blood_pressure": 80.0,
        "hypertension_medication": False,
        "fasting_glucose": 90.0,
        "glucose_lowering_medication": False,
    }
    values.update(overrides)
    return MetabolicSyndromeData(**values)


def test_metabolic_syndrome_not_calculable_if_data_is_missing() -> None:
    result = MetabolicSyndromeCalculator().calculate(MetabolicSyndromeData())

    assert result.status == CalculationStatus.NOT_CALCULABLE
    assert result.score_id == "metabolic_syndrome"


def test_metabolic_syndrome_calculates_zero_criteria() -> None:
    result = MetabolicSyndromeCalculator().calculate(_base_data())

    assert result.status == CalculationStatus.CALCULATED
    assert result.raw_value == 0
    assert result.normalized_value == 100.0
    assert result.risk_level == "Criteria threshold not met"
    assert result.attention_flags["metabolic_syndrome"] is False


def test_metabolic_syndrome_requires_three_criteria() -> None:
    result = MetabolicSyndromeCalculator().calculate(
        _base_data(
            waist_circumference=102.0,
            triglycerides=150.0,
            hdl_cholesterol=40.0,
        )
    )

    assert result.raw_value == 2
    assert result.attention_flags["waist_elevated"] is True
    assert result.attention_flags["triglycerides_elevated"] is True
    assert result.attention_flags["hdl_low"] is False
    assert result.attention_flags["metabolic_syndrome"] is False


def test_metabolic_syndrome_counts_treatment_as_criteria() -> None:
    result = MetabolicSyndromeCalculator().calculate(
        _base_data(
            waist_circumference=103.0,
            hypertension_medication=True,
            glucose_lowering_medication=True,
        )
    )

    assert result.raw_value == 3
    assert result.risk_level == "Metabolic syndrome present"
    assert result.attention_flags["metabolic_syndrome"] is True
    assert result.explanation is not None


def test_metabolic_syndrome_uses_female_thresholds() -> None:
    result = MetabolicSyndromeCalculator().calculate(
        _base_data(sex="F", waist_circumference=88.0, hdl_cholesterol=49.0)
    )

    assert result.raw_value == 2
    assert result.attention_flags["waist_elevated"] is True
    assert result.attention_flags["hdl_low"] is True
