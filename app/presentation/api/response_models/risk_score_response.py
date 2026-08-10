"""HTTP response models for the risk scoring API."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from app.domain.value_objects.score_result import CalculationStatus


class ScoreResultResponse(BaseModel):
    """Serialized form of a single score result."""

    score_id: str
    score_name: str
    domain: str
    status: CalculationStatus
    raw_value: Optional[float] = None
    normalized_value: Optional[float] = None
    risk_level: Optional[str] = None
    explanation: Optional[str] = None
    contributing_factors: dict[str, float]


class RiskAssessmentResponse(BaseModel):
    """
    Serialized form of the overall risk assessment.
    Currently only returns the individual scores.
    """

    scores: list[ScoreResultResponse]
