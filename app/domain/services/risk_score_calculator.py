"""Domain interface for risk score calculators."""

from __future__ import annotations

import abc

from app.domain.value_objects.score_result import ScoreResult


class RiskScoreCalculator[TData](abc.ABC):
    """
    Abstract base interface that all calculators must implement.
    Calculators must be stateless and specify their score-specific domain data entity.
    """

    @property
    @abc.abstractmethod
    def score_id(self) -> str:
        """Returns the unique identifier of the score this calculator computes."""
        pass

    @abc.abstractmethod
    def calculate(self, data: TData) -> ScoreResult:
        """
        Calculates the score based on the provided score-specific data.
        If required data is missing, should return a ScoreResult
        with status=CalculationStatus.NOT_CALCULABLE.
        """
        pass
