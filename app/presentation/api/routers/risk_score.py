"""Risk Score router — /api/v1/risk-score."""

from __future__ import annotations

from fastapi import APIRouter, status

from app.application.dto.risk_score_dto import ComputeRiskScoreCommand
from app.application.use_cases.compute_risk_score import ComputeRiskScoreUseCase
from app.presentation.api.dependencies import ComputeRiskScoreUseCaseDep
from app.presentation.api.request_models.risk_score_request import RiskScoreRequest
from app.presentation.api.response_models.risk_score_response import (
    RiskAssessmentResponse,
    ScoreResultResponse,
)

router = APIRouter(prefix="/api/v1/risk-score", tags=["risk-score"])


@router.post(
    "",
    response_model=RiskAssessmentResponse,
    status_code=status.HTTP_200_OK,
    summary="Compute health risk scores from the provided parameters",
)
def compute_risk_score(
    request: RiskScoreRequest,
    use_case: ComputeRiskScoreUseCase = ComputeRiskScoreUseCaseDep,
) -> RiskAssessmentResponse:
    """
    Receive health data parameters, execute the scoring engine, and return the results.
    """
    command = ComputeRiskScoreCommand(
        age=request.age,
        sex=request.sex,
        weight=request.weight,
        height=request.height,
        waist_circumference=request.waist_circumference,
        systolic_blood_pressure=request.systolic_blood_pressure,
        total_cholesterol=request.total_cholesterol,
        hdl=request.hdl,
        triglycerides=request.triglycerides,
        smoker=request.smoker,
        daily_physical_activity=request.daily_physical_activity,
        fruits_vegetables=request.fruits_vegetables,
        hypertension_medication=request.hypertension_medication,
        previous_high_glucose=request.previous_high_glucose,
        family_diabetes=request.family_diabetes,
        snoring=request.snoring,
        tired=request.tired,
        observed_apnea=request.observed_apnea,
        neck_circumference=request.neck_circumference,
    )

    result_dto = use_case.execute(command)

    # Map DTO to HTTP Response
    response_scores = [
        ScoreResultResponse(
            score_id=score.score_id,
            score_name=score.score_name,
            domain=score.domain,
            status=score.status,
            raw_value=score.raw_value,
            normalized_value=score.normalized_value,
            risk_level=score.risk_level,
            explanation=score.explanation,
            contributing_factors=score.contributing_factors,
        )
        for score in result_dto.scores
    ]

    return RiskAssessmentResponse(scores=response_scores)
