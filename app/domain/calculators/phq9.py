"""PHQ-9 (Patient Health Questionnaire-9) depression severity calculator.

Source: Kroenke K, Spitzer RL, Williams JBW. The PHQ-9: validity of a brief
depression severity measure. J Gen Intern Med. 2001;16(9):606-613.

This implementation uses the standard 9-item instrument scored 0–3 over the
previous two weeks, with published severity bands 0–4 / 5–9 / 10–14 / 15–19 /
20–27. Item 9 (thoughts of death or self-harm) is also exposed as a flag.
"""

from __future__ import annotations

from app.domain.entities.phq9_data import PHQ9_ITEM_FIELDS, Phq9Data
from app.domain.services.risk_score_calculator import RiskScoreCalculator
from app.domain.value_objects.score_result import CalculationStatus, ScoreResult

_VALID_ITEM_SCORES = {0, 1, 2, 3}
_MAX_RAW_SCORE = 27.0


def _severity_for_total(total: int) -> str:
    if total <= 4:
        return "None / minimal"
    if total <= 9:
        return "Mild"
    if total <= 14:
        return "Moderate"
    if total <= 19:
        return "Moderately severe"
    return "Severe"


class PHQ9Calculator(RiskScoreCalculator[Phq9Data]):
    """Calculates PHQ-9 depressive symptom severity."""

    @property
    def score_id(self) -> str:
        return "phq9"

    def calculate(self, data: Phq9Data) -> ScoreResult:
        item_scores: dict[str, float] = {}
        for field in PHQ9_ITEM_FIELDS:
            value = getattr(data, field)
            if value is None or value not in _VALID_ITEM_SCORES:
                return ScoreResult(
                    score_id="phq9",
                    score_name="PHQ-9",
                    domain="Depression",
                    status=CalculationStatus.NOT_CALCULABLE,
                    explanation="Missing required data for PHQ-9",
                )
            item_scores[field] = float(value)

        total_score = int(sum(item_scores.values()))
        self_harm_flag = 1.0 if item_scores["self_harm_thoughts"] > 0 else 0.0
        factors = {**item_scores, "self_harm_flag": self_harm_flag}

        explanation = None
        if self_harm_flag:
            explanation = (
                "Item 9 (thoughts of death or self-harm) is positive and "
                "requires clinical attention."
            )

        normalized_value = round(
            max(0.0, min(100.0, 100.0 - (total_score / _MAX_RAW_SCORE) * 100.0)),
            1,
        )

        return ScoreResult(
            score_id="phq9",
            score_name="PHQ-9",
            domain="Depression",
            status=CalculationStatus.CALCULATED,
            raw_value=total_score,
            normalized_value=normalized_value,
            risk_level=_severity_for_total(total_score),
            explanation=explanation,
            contributing_factors=factors,
            attention_flags={"self_harm_thoughts": bool(self_harm_flag)},
        )
