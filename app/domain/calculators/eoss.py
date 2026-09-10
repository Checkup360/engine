"""Edmonton Obesity Staging System calculator."""

from __future__ import annotations

from app.domain.entities.eoss_data import EOSSData
from app.domain.services.risk_score_calculator import RiskScoreCalculator
from app.domain.value_objects.score_result import CalculationStatus, ScoreResult

_VALID_STAGES = set(range(5))
_STAGE_LABELS = {
    0: "No risk factors or impairment",
    1: "Subclinical risk factors or mild impairment",
    2: "Established chronic disease or moderate impairment",
    3: "Significant end-organ damage or impairment",
    4: "Severe or end-stage impairment",
}


class EOSSCalculator(RiskScoreCalculator[EOSSData]):
    """Calculates the highest clinician-assessed EOSS stage."""

    @property
    def score_id(self) -> str:
        return "eoss"

    def calculate(self, data: EOSSData) -> ScoreResult:
        stages = {
            "physical_health_stage": data.physical_health_stage,
            "mental_health_stage": data.mental_health_stage,
            "functional_stage": data.functional_stage,
        }
        if any(
            value is None or value not in _VALID_STAGES for value in stages.values()
        ):
            return ScoreResult(
                score_id="eoss",
                score_name="EOSS",
                domain="Obesity-related Health Impact",
                status=CalculationStatus.NOT_CALCULABLE,
                explanation="Missing or invalid data for EOSS",
            )

        valid_stages = {
            name: value for name, value in stages.items() if value is not None
        }
        stage = max(valid_stages.values())
        return ScoreResult(
            score_id="eoss",
            score_name="EOSS",
            domain="Obesity-related Health Impact",
            status=CalculationStatus.CALCULATED,
            raw_value=stage,
            normalized_value=round(100.0 - (stage / 4.0) * 100.0, 1),
            risk_level=f"Stage {stage}",
            explanation=_STAGE_LABELS[stage],
            contributing_factors={
                **{name: float(value) for name, value in valid_stages.items()},
                "highest_stage": float(stage),
            },
            attention_flags={
                "stage_2_or_higher": stage >= 2,
                "stage_3_or_higher": stage >= 3,
                "stage_4": stage == 4,
            },
        )