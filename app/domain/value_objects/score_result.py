"""Value objects representing the result of a scoring calculation."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

MAXIMUM_SCALE_VALUE = 100.0


class CalculationStatus(StrEnum):
    """Status of a score calculation."""

    CALCULATED = "CALCULATED"
    NOT_CALCULABLE = "NOT_CALCULABLE"


@dataclass(frozen=True)
class ScoreResult:
    """
    Standardized result from any ScoreCalculator.

    Calculators express clinical severity as ``normalized_value`` (0-100,
    higher is riskier). Consumers must use ``health_index`` (0-100, higher is
    healthier), which is the only direction persisted or exposed outside the
    engine. This property is the single place in the system where risk is
    inverted.
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
    attention_flags: dict[str, bool] = field(default_factory=dict)

    @property
    def health_index(self) -> float | None:
        """Health index on a 0-100 scale where higher means healthier."""
        if self.normalized_value is None:
            return None
        return round(MAXIMUM_SCALE_VALUE - self.normalized_value, 1)
