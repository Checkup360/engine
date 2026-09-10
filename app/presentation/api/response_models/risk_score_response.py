"""HTTP response models for the risk scoring API."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from app.domain.value_objects.score_result import CalculationStatus


class ScoreResultResponse(BaseModel):
    """Serialized form of a single score result."""

    model_config = ConfigDict(from_attributes=True)

    score_id: str
    score_name: str
    domain: str
    status: CalculationStatus
    raw_value: float | None = None
    normalized_value: float | None = None
    risk_level: str | None = None
    explanation: str | None = None
    contributing_factors: dict[str, float]
    attention_flags: dict[str, bool]
