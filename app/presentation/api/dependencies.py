"""Dependency composition for the Engine API."""

from __future__ import annotations

from fastapi import Depends

from app.application.use_cases.compute_risk_score import ComputeRiskScoreUseCase
from app.domain.calculators.findrisc import FINDRISCCalculator
from app.domain.calculators.stop_bang import STOPBANGCalculator
from app.domain.services.scoring_engine import ScoringEngine


def get_scoring_engine() -> ScoringEngine:
    """Constructs the ScoringEngine with all available calculators."""
    calculators = [
        FINDRISCCalculator(),
        STOPBANGCalculator(),
    ]
    return ScoringEngine(calculators=calculators)


def get_compute_risk_score_use_case(
    engine: ScoringEngine = Depends(get_scoring_engine),  # noqa: B008
) -> ComputeRiskScoreUseCase:
    """Constructs the ComputeRiskScoreUseCase."""
    return ComputeRiskScoreUseCase(engine=engine)


ComputeRiskScoreUseCaseDep = Depends(get_compute_risk_score_use_case)
