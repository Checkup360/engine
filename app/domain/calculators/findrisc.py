"""FINDRISC (Type 2 Diabetes Risk) calculator stub."""

from __future__ import annotations

from app.domain.entities.findrisc_data import FindriscData
from app.domain.services.risk_score_calculator import RiskScoreCalculator
from app.domain.value_objects.score_result import CalculationStatus, ScoreResult


class FINDRISCCalculator(RiskScoreCalculator[FindriscData]):
    """Calculates FINDRISC diabetes risk (Type 2)."""

    @property
    def score_id(self) -> str:
        return "findrisc"

    def calculate(self, data: FindriscData) -> ScoreResult:
        # 1. Validation
        if (
            data.age is None
            or data.weight is None
            or data.height is None
            or data.sex is None
            or data.waist_circumference is None
            or data.daily_physical_activity is None
            or data.fruits_vegetables is None
            or data.hypertension_medication is None
            or data.previous_high_glucose is None
            or data.family_diabetes is None
        ):
            return ScoreResult(
                score_id="findrisc",
                score_name="FINDRISC",
                domain="Diabetes",
                status=CalculationStatus.NOT_CALCULABLE,
                explanation="Missing required data for FINDRISC",
            )

        factors: dict[str, float] = {}

        # 2. Age points
        age_pts = 0
        if 45 <= data.age <= 54:
            age_pts = 2
        elif 55 <= data.age <= 64:
            age_pts = 3
        elif data.age >= 65:
            age_pts = 4
        factors["age"] = age_pts

        # 3. BMI points
        bmi = data.weight / (data.height**2)
        bmi_pts = 0
        if 25 <= bmi < 30:
            bmi_pts = 1
        elif bmi >= 30:
            bmi_pts = 3
        factors["bmi"] = bmi_pts

        # 4. Waist Circumference points
        waist_pts = 0
        if data.sex.upper() == "M":
            if 94 <= data.waist_circumference <= 101:
                waist_pts = 3
            elif data.waist_circumference >= 102:
                waist_pts = 4
        elif data.sex.upper() == "F":
            if 80 <= data.waist_circumference <= 87:
                waist_pts = 3
            elif data.waist_circumference >= 88:
                waist_pts = 4
        factors["waist"] = waist_pts

        # 5. Physical Activity points
        pa_pts = 0 if data.daily_physical_activity else 2
        factors["physical_activity"] = pa_pts

        # 6. Fruits/Vegetables points
        fv_pts = 0 if data.fruits_vegetables else 1
        factors["fruits_vegetables"] = fv_pts

        # 7. Hypertension Medication points
        htn_pts = 2 if data.hypertension_medication else 0
        factors["hypertension"] = htn_pts

        # 8. High Glucose points
        gluc_pts = 5 if data.previous_high_glucose else 0
        factors["high_glucose"] = gluc_pts

        # 9. Family Diabetes points
        fam_pts = 0
        if data.family_diabetes == "second_degree":
            fam_pts = 3
        elif data.family_diabetes == "first_degree":
            fam_pts = 5
        factors["family_diabetes"] = fam_pts

        # Calculate Total
        total_score = sum(factors.values())

        # Determine Risk Level
        risk_level = "Unknown"
        if 0 <= total_score <= 6:
            risk_level = "Low"
        elif 7 <= total_score <= 11:
            risk_level = "Slightly elevated"
        elif 12 <= total_score <= 14:
            risk_level = "Moderate"
        elif 15 <= total_score <= 20:
            risk_level = "High"
        elif 21 <= total_score <= 26:
            risk_level = "Very high"

        normalized_value = round(max(0.0, min(100.0, 100.0 - (total_score / 26.0) * 100.0)), 1)

        return ScoreResult(
            score_id="findrisc",
            score_name="FINDRISC",
            domain="Diabetes",
            status=CalculationStatus.CALCULATED,
            raw_value=total_score,
            normalized_value=normalized_value,
            risk_level=risk_level,
            contributing_factors=factors,
        )
