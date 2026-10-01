"""AUDIT-C (WHO Alcohol Use Disorders Identification Test-Consumption) calculator."""

from __future__ import annotations

from app.domain.entities.audit_c_data import AuditCData
from app.domain.services.risk_score_calculator import RiskScoreCalculator
from app.domain.value_objects.score_result import CalculationStatus, ScoreResult

_VALID_SCORES = set(range(5))


class AuditCCalculator(RiskScoreCalculator[AuditCData]):
    """Calculates AUDIT-C alcohol consumption risk score."""

    @property
    def score_id(self) -> str:
        return "audit_c"

    def calculate(self, data: AuditCData) -> ScoreResult:
        sex = data.sex.upper() if data.sex else None
        if (
            data.frequency is None
            or data.quantity is None
            or data.heavy_drinking is None
            or data.frequency not in _VALID_SCORES
            or data.quantity not in _VALID_SCORES
            or data.heavy_drinking not in _VALID_SCORES
            or sex not in ("M", "F")
        ):
            return ScoreResult(
                score_id="audit_c",
                score_name="AUDIT-C Alcohol Risk",
                domain="Alcohol Use",
                status=CalculationStatus.NOT_CALCULABLE,
                explanation="Missing or invalid data for AUDIT-C alcohol calculation",
            )

        total_score = data.frequency + data.quantity + data.heavy_drinking
        cutoff = 4 if sex == "M" else 3
        is_positive = total_score >= cutoff

        risk_level = "High risk" if is_positive else "Low risk"
        if total_score < cutoff:
            risk_value = round((total_score / cutoff) * 50.0, 1)
        else:
            risk_value = round(
                51.0 + ((total_score - cutoff) / (12 - cutoff)) * 49.0, 1
            )

        explanation = (
            f"AUDIT-C score is {total_score}/12 "
            f"({risk_level} for {sex} threshold of {cutoff})."
        )

        factors = {
            "frequency": float(data.frequency),
            "quantity": float(data.quantity),
            "heavy_drinking": float(data.heavy_drinking),
            "sex_cutoff": float(cutoff),
        }

        return ScoreResult(
            score_id="audit_c",
            score_name="AUDIT-C Alcohol Risk",
            domain="Alcohol Use",
            status=CalculationStatus.CALCULATED,
            raw_value=float(total_score),
            risk_value=risk_value,
            risk_level=risk_level,
            explanation=explanation,
            contributing_factors=factors,
            attention_flags={
                "positive_screening": is_positive,
                "heavy_episodic_drinking": data.heavy_drinking >= 2,
            },
        )
