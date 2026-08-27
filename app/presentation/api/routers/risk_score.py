from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Path, status

from app.application.dto.risk_score_dto import ComputeRiskScoreCommand
from app.application.use_cases.compute_risk_score import ComputeRiskScoreUseCase
from app.presentation.api.dependencies import ComputeRiskScoreUseCaseDep
from app.presentation.api.request_models.risk_score_request import RiskScoreRequest
from app.presentation.api.response_models.risk_score_response import (
    ScoreResultResponse,
)

router = APIRouter(prefix="/risk-scores", tags=["risk-scores"])


@router.post(
    "/{score_id}",
    response_model=ScoreResultResponse,
    status_code=status.HTTP_200_OK,
    summary="Compute a specific health risk score from the provided parameters",
)
def compute_risk_score(
    score_id: Annotated[
        str, Path(description="The ID of the risk score model to evaluate")
    ],
    request: RiskScoreRequest,
    use_case: ComputeRiskScoreUseCase = ComputeRiskScoreUseCaseDep,
) -> ScoreResultResponse:
    """
    Receive health data parameters and a score model ID,
    execute the score calculation, and return the result.
    """
    command = ComputeRiskScoreCommand(
        score_id=score_id,
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

    result = use_case.execute(command)

    return ScoreResultResponse(
        score_id=result.score_id,
        score_name=result.score_name,
        domain=result.domain,
        status=result.status,
        raw_value=result.raw_value,
        normalized_value=result.normalized_value,
        risk_level=result.risk_level,
        explanation=result.explanation,
        contributing_factors=result.contributing_factors,
    )
