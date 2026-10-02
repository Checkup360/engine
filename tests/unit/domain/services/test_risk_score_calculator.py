from dataclasses import dataclass

import pytest

from app.domain.calculators.findrisc import FINDRISCCalculator
from app.domain.calculators.phq9 import PHQ9Calculator
from app.domain.calculators.stop_bang import STOPBANGCalculator
from app.domain.services.risk_score_calculator import RiskScoreCalculator
from app.domain.value_objects.health_topic import HealthTopic
from app.domain.value_objects.score_result import (
    CalculationStatus,
    ScoreResult,
)


@dataclass(frozen=True)
class DummyData:
    age: int | None = None


class DummyCalculator(RiskScoreCalculator[DummyData]):
    @property
    def score_id(self) -> str:
        return "dummy_score"

    @property
    def topic(self) -> HealthTopic:
        return HealthTopic(key="dummy", label="Dummy")

    def calculate(self, data: DummyData) -> ScoreResult:
        if data.age is None:
            return ScoreResult(
                score_id=self.score_id,
                score_name="Dummy Score",
                domain="General",
                status=CalculationStatus.NOT_CALCULABLE,
                explanation="Missing age",
            )
        return ScoreResult(
            score_id=self.score_id,
            score_name="Dummy Score",
            domain="General",
            status=CalculationStatus.CALCULATED,
            raw_value=float(data.age * 2),
            risk_level="Moderate",
        )


def test_cannot_instantiate_abstract_risk_score_calculator() -> None:
    with pytest.raises(TypeError):
        RiskScoreCalculator()  # type: ignore[abstract]


def test_dummy_calculator_implements_interface() -> None:
    calc = DummyCalculator()
    assert isinstance(calc, RiskScoreCalculator)
    assert calc.score_id == "dummy_score"

    res = calc.calculate(DummyData(age=25))
    assert isinstance(res, ScoreResult)
    assert res.status == CalculationStatus.CALCULATED
    assert res.raw_value == 50.0
    assert res.risk_level == "Moderate"


def test_findrisc_implements_risk_score_calculator() -> None:
    calc = FINDRISCCalculator()
    assert isinstance(calc, RiskScoreCalculator)
    assert calc.score_id == "findrisc"


def test_stop_bang_implements_risk_score_calculator() -> None:
    calc = STOPBANGCalculator()
    assert isinstance(calc, RiskScoreCalculator)
    assert calc.score_id == "stop_bang"


def test_phq9_implements_risk_score_calculator() -> None:
    calc = PHQ9Calculator()
    assert isinstance(calc, RiskScoreCalculator)
    assert calc.score_id == "phq9"
