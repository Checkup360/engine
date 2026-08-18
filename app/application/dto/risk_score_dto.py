"""DTOs for the risk scoring application layer."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.value_objects.score_result import ScoreResult


@dataclass(frozen=True)
class ComputeRiskScoreCommand:
    """Command to compute the risk score."""

    age: int | None = None
    sex: str | None = None
    weight: float | None = None
    height: float | None = None
    waist_circumference: float | None = None
    systolic_blood_pressure: float | None = None
    total_cholesterol: float | None = None
    hdl: float | None = None
    triglycerides: float | None = None
    smoker: bool | None = None
    daily_physical_activity: bool | None = None
    fruits_vegetables: bool | None = None
    hypertension_medication: bool | None = None
    previous_high_glucose: bool | None = None
    family_diabetes: str | None = None
    snoring: bool | None = None
    tired: bool | None = None
    observed_apnea: bool | None = None
    neck_circumference: float | None = None
    target_scores: list[str] | None = None


@dataclass(frozen=True)
class RiskAssessmentDTO:
    """
    Application response for a risk assessment.
    For now, it only contains the list of individual score results.
    Later it will include the aggregated overall score.
    """

    scores: list[ScoreResult]
