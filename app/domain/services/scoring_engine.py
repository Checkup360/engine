"""Scoring Engine domain service."""

from __future__ import annotations

from collections.abc import Sequence

from app.domain.calculators.base import ScoreCalculator
from app.domain.entities.employee_health_data import EmployeeHealthData
from app.domain.value_objects.score_result import ScoreResult


class ScoringEngine:
    """
    Orchestrates the execution of multiple ScoreCalculators.
    """

    def __init__(self, calculators: Sequence[ScoreCalculator]) -> None:
        """
        Initializes the engine with a list of calculators to execute.
        This allows injecting any combination of calculators without modifying
        the engine.
        """
        self._calculators = calculators

    def compute_scores(
        self, data: EmployeeHealthData, target_scores: list[str] | None = None
    ) -> list[ScoreResult]:
        """
        Executes all configured calculators and returns their results.
        If target_scores is provided, executes only matching score_ids.
        """
        results: list[ScoreResult] = []
        for calculator in self._calculators:
            if target_scores and calculator.score_id not in target_scores:
                continue
            result = calculator.calculate(data)
            results.append(result)

        return results
