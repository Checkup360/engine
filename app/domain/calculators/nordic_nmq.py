"""Standardized Nordic Questionnaire (NMQ) Ergonomic Risk calculator."""

from __future__ import annotations

from app.domain.entities.nordic_nmq_data import NMQ_ANATOMICAL_ZONES, NordicNmqData
from app.domain.services.risk_score_calculator import RiskScoreCalculator
from app.domain.value_objects.health_topic import HealthTopic
from app.domain.value_objects.score_result import CalculationStatus, ScoreResult


class NordicNMQCalculator(RiskScoreCalculator[NordicNmqData]):
    """Calculates Ergonomic / Musculoskeletal risk using the Nordic Questionnaire."""

    @property
    def score_id(self) -> str:
        return "nordic_nmq"

    @property
    def topic(self) -> HealthTopic:
        return HealthTopic(key="nordic_nmq", label="Musculoskeletal Health")

    def calculate(self, data: NordicNmqData) -> ScoreResult:
        if not data.zones or len(data.zones) < len(NMQ_ANATOMICAL_ZONES):
            return ScoreResult(
                score_id="nordic_nmq",
                score_name="Standardized Nordic Questionnaire (NMQ)",
                domain="Ergonomics",
                status=CalculationStatus.NOT_CALCULABLE,
                explanation="Missing data for one or more anatomical zones in NMQ",
            )

        has_work_impediment = False
        has_recent_7day_pain = False
        has_12month_pain = False
        total_positive_responses = 0

        factors: dict[str, float] = {}

        for zone_key in NMQ_ANATOMICAL_ZONES:
            zone_data = data.zones.get(zone_key)
            if (
                zone_data is None
                or zone_data.trouble_last_12_months is None
                or zone_data.prevented_work_last_12_months is None
                or zone_data.trouble_last_7_days is None
            ):
                return ScoreResult(
                    score_id="nordic_nmq",
                    score_name="Standardized Nordic Questionnaire (NMQ)",
                    domain="Ergonomics",
                    status=CalculationStatus.NOT_CALCULABLE,
                    explanation=f"Missing data for anatomical zone: {zone_key}",
                )

            if zone_data.trouble_last_12_months:
                has_12month_pain = True
                total_positive_responses += 1

            if zone_data.prevented_work_last_12_months:
                has_work_impediment = True
                total_positive_responses += 1

            if zone_data.trouble_last_7_days:
                has_recent_7day_pain = True
                total_positive_responses += 1

            factors[f"{zone_key}_12m_trouble"] = (
                1.0 if zone_data.trouble_last_12_months else 0.0
            )
            factors[f"{zone_key}_12m_work_prevented"] = (
                1.0 if zone_data.prevented_work_last_12_months else 0.0
            )
            factors[f"{zone_key}_7d_trouble"] = (
                1.0 if zone_data.trouble_last_7_days else 0.0
            )

        # Domain scoring rules:
        # 1. High Risk (Red): Q2 prevented work in last 12m in ANY zone.
        # 2. Moderate Risk (Yellow): Q3 recent 7-day pain in ANY zone
        #    without Q2 work impediment.
        # 3. Low Risk (Green): Q2 and Q3 all False.
        if has_work_impediment:
            risk_level = "High risk"
            risk_value = 100.0
            explanation = (
                "High ergonomic risk: Work impediment reported in "
                "one or more anatomical zones."
            )
        elif has_recent_7day_pain:
            risk_level = "Moderate risk"
            risk_value = 50.0
            explanation = (
                "Moderate ergonomic risk: Recent pain reported in "
                "last 7 days without work impediment."
            )
        else:
            risk_level = "Low risk"
            risk_value = 0.0
            explanation = (
                "Low ergonomic risk: No recent pain or work impediment reported."
            )

        return ScoreResult(
            score_id="nordic_nmq",
            score_name="Standardized Nordic Questionnaire (NMQ)",
            domain="Ergonomics",
            status=CalculationStatus.CALCULATED,
            raw_value=float(total_positive_responses),
            risk_value=risk_value,
            risk_level=risk_level,
            explanation=explanation,
            contributing_factors=factors,
            attention_flags={
                "has_work_impediment": has_work_impediment,
                "has_recent_7day_pain": has_recent_7day_pain,
                "has_12month_pain": has_12month_pain,
            },
        )
