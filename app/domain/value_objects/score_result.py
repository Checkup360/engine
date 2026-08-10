"""Value objects representing the result of a scoring calculation."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class CalculationStatus(str, Enum):
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
    raw_value: Optional[float] = None
    normalized_value: Optional[float] = None
    risk_level: Optional[str] = None
    explanation: Optional[str] = None
    contributing_factors: dict[str, float] = field(default_factory=dict)
