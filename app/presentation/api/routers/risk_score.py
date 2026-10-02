"""Risk Score router — /risk-scores."""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, Path, status

from app.application.use_cases.compute_risk_score import ComputeRiskScoreUseCase
from app.domain.exceptions import ScoreCalculatorNotFoundError
from app.domain.services.scoring_engine import ScoringEngine
from app.presentation.api.dependencies import (
    ComputeRiskScoreUseCaseDep,
    get_scoring_engine,
)
from app.presentation.api.request_models.registry import (
    get_catalog,
    get_request_model,
)
from app.presentation.api.response_models.catalog_response import (
    ScoreCatalogItemResponse,
)
from app.presentation.api.response_models.risk_score_response import (
    ScoreResultResponse,
)

router = APIRouter(prefix="/risk-scores", tags=["risk-scores"])


@router.get(
    "/catalog",
    response_model=list[ScoreCatalogItemResponse],
    status_code=status.HTTP_200_OK,
    summary="Get catalog of available risk scores and required fields",
)
def get_score_catalog(
    engine: Annotated[ScoringEngine, Depends(get_scoring_engine)],
) -> list[ScoreCatalogItemResponse]:
    """Returns the list of available risk score calculators,
    their health topic and their required parameters."""
    return get_catalog(engine.topics_by_score())


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
    payload: Annotated[
        dict[str, Any],
        Body(description="Health parameters for the requested score"),
    ],
    use_case: ComputeRiskScoreUseCase = ComputeRiskScoreUseCaseDep,
) -> ScoreResultResponse:
    """
    Receive health data parameters for a specific score model ID,
    validate against the model's dedicated schema, and return the score result.
    """
    request_cls = get_request_model(score_id)
    if request_cls is None:
        raise ScoreCalculatorNotFoundError(f"Score calculator '{score_id}' not found.")

    # Validate against score-specific request schema
    validated_request: Any = request_cls.model_validate(payload)
    domain_data = validated_request.to_domain()

    result = use_case.execute(score_id=score_id, data=domain_data)

    return ScoreResultResponse.model_validate(result)
