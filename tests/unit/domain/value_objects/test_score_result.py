"""Unit tests for ScoreResult value object."""

from dataclasses import FrozenInstanceError

import pytest

from app.domain.value_objects.score_result import (
    CalculationStatus,
    ScoreResult,
)


def test_score_result_creation() -> None:
    res = ScoreResult(
        score_id="sample_score",
        score_name="Sample Score",
        domain="Cardiovascular",
        status=CalculationStatus.CALCULATED,
        raw_value=15.5,
        risk_level="High",
    )
    assert res.score_id == "sample_score"
    assert res.score_name == "Sample Score"
    assert res.domain == "Cardiovascular"
    assert res.status == CalculationStatus.CALCULATED
    assert res.raw_value == 15.5
    assert res.risk_level == "High"


def test_score_result_not_calculable() -> None:
    res = ScoreResult(
        score_id="sample_score",
        score_name="Sample Score",
        domain="Cardiovascular",
        status=CalculationStatus.NOT_CALCULABLE,
        explanation="Missing blood pressure",
    )
    assert res.status == CalculationStatus.NOT_CALCULABLE
    assert res.raw_value is None
    assert res.explanation == "Missing blood pressure"


def test_score_result_is_frozen() -> None:
    res = ScoreResult(
        score_id="sample_score",
        score_name="Sample Score",
        domain="Cardiovascular",
        status=CalculationStatus.CALCULATED,
        raw_value=10.0,
    )
    with pytest.raises(FrozenInstanceError):
        res.raw_value = 20.0  # type: ignore[misc]


@pytest.mark.parametrize(
    "risk_value,expected_health_index",
    [(0.0, 100.0), (100.0, 0.0), (37.5, 62.5), (25.8, 74.2)],
)
def test_health_index_inverts_risk_value(
    risk_value: float, expected_health_index: float
) -> None:
    res = ScoreResult(
        score_id="sample_score",
        score_name="Sample Score",
        domain="Cardiovascular",
        status=CalculationStatus.CALCULATED,
        normalized_value=risk_value,
    )
    assert res.health_index == expected_health_index


def test_health_index_is_none_when_not_calculable() -> None:
    res = ScoreResult(
        score_id="sample_score",
        score_name="Sample Score",
        domain="Cardiovascular",
        status=CalculationStatus.NOT_CALCULABLE,
    )
    assert res.health_index is None
