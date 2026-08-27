"""Scoring Engine domain service."""

from __future__ import annotations

from collections.abc import Sequence

from app.domain.entities.employee_health_data import EmployeeHealthData
from app.domain.exceptions import ScoreCalculatorNotFoundError
from app.domain.services.risk_score_calculator import RiskScoreCalculator
from app.domain.value_objects.score_result import ScoreResult


class ScoringEngine:
    """
    Orchestrates the execution of RiskScoreCalculators.
    """

    def __init__(self, calculators: Sequence[RiskScoreCalculator]) -> None:
        """
        Initializes the engine with a sequence of calculators.
        """
        self._calculators: dict[str, RiskScoreCalculator] = {
            calc.score_id: calc for calc in calculators
        }

    def compute_score(self, score_id: str, data: EmployeeHealthData) -> ScoreResult:
        """
        Executes a single configured calculator by score_id.
        Raises ScoreCalculatorNotFoundError if score_id is not registered.
        """
        calculator = self._calculators.get(score_id)
        if calculator is None:
            raise ScoreCalculatorNotFoundError(
                f"Score calculator '{score_id}' not found."
            )
        return calculator.calculate(data)

    def compute_scores(
        self, data: EmployeeHealthData, target_scores: list[str] | None = None
    ) -> list[ScoreResult]:
        """
        Executes configured calculators and returns their results.
        If target_scores is provided, executes only matching score_ids.
        """
        results: list[ScoreResult] = []
        for score_id, calculator in self._calculators.items():
            if target_scores and score_id not in target_scores:
                continue
            result = calculator.calculate(data)
            results.append(result)

        return results
