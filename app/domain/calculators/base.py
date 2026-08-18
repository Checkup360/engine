"""Base class for all score calculators."""

from __future__ import annotations

import abc

from app.domain.entities.employee_health_data import EmployeeHealthData
from app.domain.value_objects.score_result import ScoreResult


class ScoreCalculator(abc.ABC):
    """
    Abstract base class that all calculators must implement.
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
