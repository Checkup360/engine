"""Use case for computing a specific health risk score."""

from __future__ import annotations

from typing import Any

from app.domain.services.scoring_engine import ScoringEngine
from app.domain.value_objects.score_result import ScoreResult


class ComputeRiskScoreUseCase:
    """
    Orchestrates the risk scoring process for a specific model.
    """

    def __init__(self, engine: ScoringEngine) -> None:
        self._engine = engine

    def execute(self, score_id: str, data: Any) -> ScoreResult:
        """
        Executes the scoring engine for the requested score_id
        with the provided score-specific domain data.
        """
        return self._engine.compute_score(score_id=score_id, data=data)
