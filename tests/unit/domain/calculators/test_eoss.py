"""Unit tests for EOSSCalculator."""

from app.domain.calculators.eoss import EOSSCalculator
from app.domain.entities.eoss_data import EOSSData
from app.domain.value_objects.score_result import CalculationStatus


def test_eoss_not_calculable_if_data_is_missing() -> None:
    result = EOSSCalculator().calculate(EOSSData())

    assert result.status == CalculationStatus.NOT_CALCULABLE
    assert result.score_id == "eoss"


def test_eoss_returns_highest_domain_stage() -> None:
    result = EOSSCalculator().calculate(
        EOSSData(physical_health_stage=1, mental_health_stage=3, functional_stage=2)
    )

    assert result.status == CalculationStatus.CALCULATED
    assert result.raw_value == 3
    assert result.normalized_value == 75.0
    assert result.risk_level == "High risk"
    assert result.attention_flags["stage_2_or_higher"] is True
    assert result.attention_flags["stage_3_or_higher"] is True
    assert result.attention_flags["stage_4"] is False


def test_eoss_stage_zero_is_lowest_impact() -> None:
    result = EOSSCalculator().calculate(
        EOSSData(physical_health_stage=0, mental_health_stage=0, functional_stage=0)
    )

    assert result.raw_value == 0
    assert result.normalized_value == 0.0
    assert result.risk_level == "Low risk"
    assert result.explanation == "Stage 0: No risk factors or impairment"
    assert result.attention_flags["stage_2_or_higher"] is False


def test_eoss_rejects_out_of_range_stage() -> None:
    result = EOSSCalculator().calculate(
        EOSSData(physical_health_stage=5, mental_health_stage=0, functional_stage=0)
    )

    assert result.status == CalculationStatus.NOT_CALCULABLE
