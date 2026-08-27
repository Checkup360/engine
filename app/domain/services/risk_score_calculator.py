"""Domain interface for risk score calculators."""

from __future__ import annotations

import abc

from app.domain.entities.employee_health_data import EmployeeHealthData
from app.domain.value_objects.score_result import ScoreResult


class RiskScoreCalculator(abc.ABC):
    """
    Abstract base interface that all calculators must implement.
    Calculators must be stateless.
    """

    @property
    @abc.abstractmethod
    def score_id(self) -> str:
        """Returns the unique identifier of the score this calculator computes."""
        pass

    @abc.abstractmethod
    def calculate(self, data: EmployeeHealthData) -> ScoreResult:
        """
        Calculates the score based on the provided data.
        If required data is missing, should return a ScoreResult
        with status=CalculationStatus.NOT_CALCULABLE.
        """
        pass
