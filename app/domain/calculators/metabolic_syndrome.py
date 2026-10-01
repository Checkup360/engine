"""AHA/NHLBI metabolic syndrome criteria calculator."""

from __future__ import annotations

from app.domain.entities.metabolic_syndrome_data import MetabolicSyndromeData
from app.domain.services.risk_score_calculator import RiskScoreCalculator
from app.domain.value_objects.score_result import CalculationStatus, ScoreResult

_WAIST_THRESHOLDS = {"M": 102.0, "F": 88.0}
_TRIGLYCERIDES_THRESHOLD = 150.0
_HDL_THRESHOLDS = {"M": 40.0, "F": 50.0}
_SYSTOLIC_BLOOD_PRESSURE_THRESHOLD = 130.0
_DIASTOLIC_BLOOD_PRESSURE_THRESHOLD = 85.0
_FASTING_GLUCOSE_THRESHOLD = 100.0
_METABOLIC_SYNDROME_THRESHOLD = 3


class MetabolicSyndromeCalculator(RiskScoreCalculator[MetabolicSyndromeData]):
    """Calculates the number of AHA metabolic syndrome criteria met."""

    @property
    def score_id(self) -> str:
        return "metabolic_syndrome"

    def calculate(self, data: MetabolicSyndromeData) -> ScoreResult:
        sex = data.sex.upper() if data.sex is not None else None
        if (
            sex not in _WAIST_THRESHOLDS
            or data.waist_circumference is None
            or data.triglycerides is None
            or data.hdl_cholesterol is None
            or data.systolic_blood_pressure is None
            or data.diastolic_blood_pressure is None
            or data.hypertension_medication is None
            or data.fasting_glucose is None
            or data.glucose_lowering_medication is None
        ):
            return ScoreResult(
                score_id="metabolic_syndrome",
                score_name="Metabolic Syndrome",
                domain="Metabolic Health",
                status=CalculationStatus.NOT_CALCULABLE,
                explanation="Missing required data for metabolic syndrome",
            )

        criteria = {
            "waist_elevated": data.waist_circumference >= _WAIST_THRESHOLDS[sex],
            "triglycerides_elevated": (data.triglycerides >= _TRIGLYCERIDES_THRESHOLD),
            "hdl_low": data.hdl_cholesterol < _HDL_THRESHOLDS[sex],
            "blood_pressure_elevated": (
                data.systolic_blood_pressure >= _SYSTOLIC_BLOOD_PRESSURE_THRESHOLD
                or data.diastolic_blood_pressure >= _DIASTOLIC_BLOOD_PRESSURE_THRESHOLD
                or data.hypertension_medication
            ),
            "fasting_glucose_elevated": (
                data.fasting_glucose >= _FASTING_GLUCOSE_THRESHOLD
                or data.glucose_lowering_medication
            ),
        }
        criteria_met = sum(criteria.values())
        metabolic_syndrome = criteria_met >= _METABOLIC_SYNDROME_THRESHOLD

        if metabolic_syndrome:
            risk_level = "High risk"
            explanation = (
                f"Metabolic syndrome present ({criteria_met} of 5 criteria met)."
            )
        elif criteria_met == 2:
            risk_level = "Moderate risk"
            explanation = f"Moderate metabolic risk ({criteria_met} of 5 criteria met)."
        elif criteria_met == 1:
            risk_level = "Low risk"
            explanation = f"Low metabolic risk ({criteria_met} of 5 criteria met)."
        else:
            risk_level = "Low risk"
            explanation = "Optimal metabolic health (no criteria met)."

        return ScoreResult(
            score_id="metabolic_syndrome",
            score_name="Metabolic Syndrome",
            domain="Metabolic Health",
            status=CalculationStatus.CALCULATED,
            raw_value=criteria_met,
            risk_value=round((criteria_met / 5.0) * 100.0, 1),
            risk_level=risk_level,
            explanation=explanation,
            contributing_factors={
                **{name: float(value) for name, value in criteria.items()},
                "criteria_met": float(criteria_met),
            },
            attention_flags={
                **criteria,
                "metabolic_syndrome": metabolic_syndrome,
            },
        )
