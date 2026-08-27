"""HTTP response models for the risk scoring API."""

from __future__ import annotations

from pydantic import BaseModel

from app.domain.value_objects.score_result import CalculationStatus


class ScoreResultResponse(BaseModel):
    """Serialized form of a single score result."""

    score_id: str
    score_name: str
    domain: str
    status: CalculationStatus
    raw_value: float | None = None
    normalized_value: float | None = None
    risk_level: str | None = None
    explanation: str | None = None
    contributing_factors: dict[str, float]
