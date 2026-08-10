"""Value objects representing the result of a scoring calculation."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class CalculationStatus(StrEnum):
    """Status of a score calculation."""

    CALCULATED = "CALCULATED"
    NOT_CALCULABLE = "NOT_CALCULABLE"


@dataclass(frozen=True)
class ScoreResult:
    """
    Standardized result from any ScoreCalculator.
    """

    score_id: str
    score_name: str
    domain: str
    status: CalculationStatus
    raw_value: float | None = None
    normalized_value: float | None = None
    risk_level: str | None = None
    explanation: str | None = None
    contributing_factors: dict[str, float] = field(default_factory=dict)
