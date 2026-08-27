from dataclasses import dataclass

import pytest

from app.domain.exceptions import ScoreCalculatorNotFoundError
from app.domain.services.risk_score_calculator import RiskScoreCalculator
from app.domain.services.scoring_engine import ScoringEngine
from app.domain.value_objects.score_result import CalculationStatus, ScoreResult


@dataclass(frozen=True)
class MockData:
    value: int = 1


class MockCalculator(RiskScoreCalculator[MockData]):
    def __init__(self, score_id_val: str) -> None:
        self._score_id = score_id_val

    @property
    def score_id(self) -> str:
        return self._score_id

    def calculate(self, data: MockData) -> ScoreResult:
        return ScoreResult(
            score_id=self.score_id,
            score_name=f"Mock {self.score_id}",
            domain="Mock Domain",
            status=CalculationStatus.CALCULATED,
            raw_value=42.0,
        )


def test_scoring_engine_computes_single_score() -> None:
    calc1 = MockCalculator("calc1")
    calc2 = MockCalculator("calc2")
    engine = ScoringEngine(calculators=[calc1, calc2])
    data = MockData()

    result = engine.compute_score("calc1", data)

    assert result.score_id == "calc1"
    assert result.raw_value == 42.0
    assert result.status == CalculationStatus.CALCULATED


def test_scoring_engine_raises_error_when_score_not_found() -> None:
    calc1 = MockCalculator("calc1")
    engine = ScoringEngine(calculators=[calc1])
    data = MockData()

    with pytest.raises(ScoreCalculatorNotFoundError) as exc_info:
        engine.compute_score("unknown_score", data)

    assert "unknown_score" in str(exc_info.value)
