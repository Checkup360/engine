"""DTOs for the risk scoring application layer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from app.domain.value_objects.score_result import ScoreResult


@dataclass(frozen=True)
class ComputeRiskScoreCommand:
    """Command to compute the risk score."""

    age: Optional[int] = None
    sex: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    waist_circumference: Optional[float] = None
    systolic_blood_pressure: Optional[float] = None
    total_cholesterol: Optional[float] = None
    hdl: Optional[float] = None
    triglycerides: Optional[float] = None
    smoker: Optional[bool] = None
    daily_physical_activity: Optional[bool] = None
    fruits_vegetables: Optional[bool] = None
    hypertension_medication: Optional[bool] = None
    previous_high_glucose: Optional[bool] = None
    family_diabetes: Optional[str] = None
    snoring: Optional[bool] = None
    tired: Optional[bool] = None
    observed_apnea: Optional[bool] = None
    neck_circumference: Optional[float] = None


@dataclass(frozen=True)
class RiskAssessmentDTO:
    """
    Application response for a risk assessment.
    For now, it only contains the list of individual score results.
    Later it will include the aggregated overall score.
    """

    scores: list[ScoreResult]
