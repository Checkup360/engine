"""Scoring Engine domain service."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from app.domain.exceptions import ScoreCalculatorNotFoundError
from app.domain.services.risk_score_calculator import RiskScoreCalculator
from app.domain.value_objects.score_result import ScoreResult


class ScoringEngine:
    """
    Orchestrates the execution of RiskScoreCalculators.
    """

    def __init__(self, calculators: Sequence[RiskScoreCalculator[Any]]) -> None:
        """
        Initializes the engine with a sequence of calculators.
        """
        self._calculators: dict[str, RiskScoreCalculator[Any]] = {
            calc.score_id: calc for calc in calculators
        }

    def compute_score(self, score_id: str, data: Any) -> ScoreResult:
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
