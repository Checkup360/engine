"""Unit tests for the ScoringEngine."""

from typing import Sequence

from app.domain.calculators.base import ScoreCalculator
from app.domain.entities.employee_health_data import EmployeeHealthData
from app.domain.services.scoring_engine import ScoringEngine
from app.domain.value_objects.score_result import CalculationStatus, ScoreResult


class MockCalculator(ScoreCalculator):
    def __init__(self, score_id: str) -> None:
        self.score_id = score_id

    def calculate(self, data: EmployeeHealthData) -> ScoreResult:
        return ScoreResult(
            score_id=self.score_id,
            score_name=f"Mock {self.score_id}",
            domain="Mock Domain",
            status=CalculationStatus.CALCULATED,
            raw_value=42.0,
        )


def test_scoring_engine_computes_all_calculators() -> None:
    calc1 = MockCalculator("calc1")
    calc2 = MockCalculator("calc2")
    engine = ScoringEngine(calculators=[calc1, calc2])
    data = EmployeeHealthData()

    results = engine.compute_scores(data)

    assert len(results) == 2
    assert results[0].score_id == "calc1"
    assert results[1].score_id == "calc2"
    assert results[0].raw_value == 42.0
