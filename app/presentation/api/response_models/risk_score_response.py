"""HTTP response models for the risk scoring API."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.domain.value_objects.score_result import CalculationStatus


class ScoreResultResponse(BaseModel):
    """Serialized form of a single score result."""

    model_config = ConfigDict(from_attributes=True)

    score_id: str
    score_name: str
    domain: str
    status: CalculationStatus
    raw_value: float | None = None
    health_index: float | None = Field(
        default=None,
        description="Health index from 0 to 100 where higher means healthier.",
    )
    risk_level: str | None = None
    explanation: str | None = None
    contributing_factors: dict[str, float]
    attention_flags: dict[str, bool]
