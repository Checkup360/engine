"""PSS-10 (Perceived Stress Scale-10) calculator."""

from __future__ import annotations

from app.domain.entities.pss10_data import (
    PSS10_ALL_FIELDS,
    PSS10_REVERSED_ITEMS,
    Pss10Data,
)
from app.domain.services.risk_score_calculator import RiskScoreCalculator
from app.domain.value_objects.score_result import CalculationStatus, ScoreResult

_VALID_SCORES = set(range(5))


class PSS10Calculator(RiskScoreCalculator[Pss10Data]):
    """Calculates PSS-10 perceived stress and burnout score with item reversal."""

    @property
    def score_id(self) -> str:
        return "pss10"

    def calculate(self, data: Pss10Data) -> ScoreResult:
        factors: dict[str, float] = {}
        total_score = 0

        for field_name in PSS10_ALL_FIELDS:
            value = getattr(data, field_name)
            if value is None or value not in _VALID_SCORES:
                return ScoreResult(
                    score_id="pss10",
                    score_name="PSS-10 Perceived Stress Scale",
                    domain="Psychological Health",
                    status=CalculationStatus.NOT_CALCULABLE,
                    explanation=f"Missing or invalid response for PSS-10 item: {field_name}",
                )

            # Mathematical item reversal for questions 4, 5, 7, 8 (4 - value)
            if field_name in PSS10_REVERSED_ITEMS:
                processed_score = 4 - int(value)
            else:
                processed_score = int(value)

            factors[field_name] = float(processed_score)
            total_score += processed_score

        if total_score <= 13:
            risk_level = "Low risk"
            explanation = f"Low perceived stress (Score {total_score}/40)."
            normalized_value = round((total_score / 13) * 20.0, 1) if total_score > 0 else 0.0
        elif total_score <= 26:
            risk_level = "Moderate risk"
            explanation = f"Moderate perceived stress (Score {total_score}/40)."
            normalized_value = round(21.0 + ((total_score - 14) / 12.0) * 29.0, 1)
        else:
            risk_level = "High risk"
            explanation = f"Severe perceived stress / burnout risk (Score {total_score}/40)."
            normalized_value = round(51.0 + ((total_score - 27) / 13.0) * 49.0, 1)

        return ScoreResult(
            score_id="pss10",
            score_name="PSS-10 Perceived Stress Scale",
            domain="Psychological Health",
            status=CalculationStatus.CALCULATED,
            raw_value=float(total_score),
            normalized_value=normalized_value,
            risk_level=risk_level,
            explanation=explanation,
            contributing_factors=factors,
            attention_flags={
                "severe_stress_or_burnout": total_score >= 27,
                "moderate_or_higher_stress": total_score >= 14,
            },
        )
