"""STOP-BANG (Sleep Apnea Screening) calculator."""

from __future__ import annotations

from app.domain.entities.stop_bang_data import StopBangData
from app.domain.services.risk_score_calculator import RiskScoreCalculator
from app.domain.value_objects.score_result import CalculationStatus, ScoreResult


class STOPBANGCalculator(RiskScoreCalculator[StopBangData]):
    """Calculates STOP-BANG risk for sleep apnea screening."""

    @property
    def score_id(self) -> str:
        return "stop_bang"

    def calculate(self, data: StopBangData) -> ScoreResult:
        # 1. Validation
        if (
            data.snoring is None
            or data.tired is None
            or data.observed_apnea is None
            or data.hypertension_medication is None
            or data.weight is None
            or data.height is None
            or data.age is None
            or data.neck_circumference is None
            or data.sex is None
        ):
            return ScoreResult(
                score_id="stop_bang",
                score_name="STOP-BANG",
                domain="Sleep Apnea",
                status=CalculationStatus.NOT_CALCULABLE,
                explanation="Missing required data for STOP-BANG",
            )

        factors: dict[str, float] = {}
        total_score = 0

        # S - Snoring
        pts = 1 if data.snoring else 0
        factors["snoring"] = pts
        total_score += pts

        # T - Tired
        pts = 1 if data.tired else 0
        factors["tired"] = pts
        total_score += pts

        # O - Observed apnea
        pts = 1 if data.observed_apnea else 0
        factors["observed_apnea"] = pts
        total_score += pts

        # P - Pressure (Hypertension)
        pts = 1 if data.hypertension_medication else 0
        factors["pressure"] = pts
        total_score += pts

        # B - BMI > 35
        bmi = data.weight / (data.height**2)
        pts = 1 if bmi > 35 else 0
        factors["bmi"] = pts
        total_score += pts

        # A - Age > 50
        pts = 1 if data.age > 50 else 0
        factors["age"] = pts
        total_score += pts

        # N - Neck circumference > 40 cm
        pts = 1 if data.neck_circumference > 40 else 0
        factors["neck"] = pts
        total_score += pts

        # G - Gender = Male
        pts = 1 if data.sex.upper() == "M" else 0
        factors["gender"] = pts
        total_score += pts

        # Interpretation
        risk_level = "Unknown"
        if 0 <= total_score <= 2:
            risk_level = "Low"
        elif 3 <= total_score <= 4:
            risk_level = "Intermediate"
        elif 5 <= total_score <= 8:
            risk_level = "High"

        normalized_value = round(max(0.0, min(100.0, 100.0 - (total_score / 8.0) * 100.0)), 1)

        return ScoreResult(
            score_id="stop_bang",
            score_name="STOP-BANG",
            domain="Sleep Apnea",
            status=CalculationStatus.CALCULATED,
            raw_value=total_score,
            normalized_value=normalized_value,
            risk_level=risk_level,
            contributing_factors=factors,
        )
