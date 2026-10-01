"""SCORE2 European cardiovascular risk calculator.

Derived from ESC / SCORE2 Working Group, European Heart Journal (2021).
Calculates 10-year risk of a first fatal or non-fatal cardiovascular disease
event in adults aged 40-69 using sex-specific competing-risk equations and
regional recalibration.
"""

from __future__ import annotations

import math

from app.domain.entities.score2_data import Score2Data
from app.domain.services.risk_score_calculator import RiskScoreCalculator
from app.domain.value_objects.score_result import CalculationStatus, ScoreResult

# Baseline survival S0 at 10 years
_S0 = {
    "M": 0.9605,
    "F": 0.9776,
}

# Calibration scale parameters (scale1, scale2) by risk region and sex
_REGIONAL_SCALES: dict[str, dict[str, tuple[float, float]]] = {
    "low": {
        "M": (-0.5699, 0.7476),
        "F": (-0.7380, 0.7019),
    },
    "moderate": {
        "M": (-0.1565, 0.8009),
        "F": (-0.3143, 0.7701),
    },
    "high": {
        "M": (0.3207, 0.9360),
        "F": (0.5710, 0.9369),
    },
    "very_high": {
        "M": (0.5836, 0.8294),
        "F": (0.9412, 0.8329),
    },
}

# Conversion factor from mg/dL to mmol/L for cholesterol
_MG_DL_TO_MMOL_L = 38.67

# 10-year CVD risk ≥30% is treated as maximum severity for the 0-100 UI scale;
# SCORE2's own risk bands already classify >=20% as "Very high risk".
_NORMALIZATION_RISK_CEILING_PERCENT = 30.0


def _to_mmol_l(val: float, mg_dl_threshold: float) -> float:
    """Converts cholesterol from mg/dL to mmol/L if value exceeds threshold."""
    if val > mg_dl_threshold:
        return val / _MG_DL_TO_MMOL_L
    return val


class SCORE2Calculator(RiskScoreCalculator[Score2Data]):
    """Calculates the 10-year fatal/non-fatal cardiovascular risk via SCORE2."""

    @property
    def score_id(self) -> str:
        return "score2"

    def calculate(self, data: Score2Data) -> ScoreResult:
        sex = data.sex.upper() if data.sex is not None else None
        region = (data.risk_region or "moderate").lower()

        if (
            sex not in ("M", "F")
            or region not in _REGIONAL_SCALES
            or data.age is None
            or data.smoker is None
            or data.systolic_blood_pressure is None
            or data.total_cholesterol is None
            or data.hdl_cholesterol is None
        ):
            return ScoreResult(
                score_id="score2",
                score_name="SCORE2",
                domain="Cardiovascular",
                status=CalculationStatus.NOT_CALCULABLE,
                explanation=(
                    "Missing required data for SCORE2 cardiovascular risk calculation."
                ),
            )

        # Standardize cholesterol units to mmol/L
        total_chol_mmol = _to_mmol_l(data.total_cholesterol, mg_dl_threshold=20.0)
        hdl_chol_mmol = _to_mmol_l(data.hdl_cholesterol, mg_dl_threshold=10.0)

        # Centered variables
        cage = (float(data.age) - 60.0) / 5.0
        csbp = (float(data.systolic_blood_pressure) - 120.0) / 20.0
        ctchol = (total_chol_mmol - 6.0) / 1.0
        chdl = (hdl_chol_mmol - 1.3) / 0.5
        smoking = 1.0 if data.smoker else 0.0

        # Linear predictor (lp) sex-specific equations
        if sex == "M":
            lp = (
                0.3742 * cage
                + 0.6012 * smoking
                + 0.2777 * csbp
                + 0.1458 * ctchol
                - 0.2698 * chdl
                - 0.0755 * cage * smoking
                - 0.0255 * cage * csbp
                - 0.0281 * cage * ctchol
                + 0.0426 * cage * chdl
            )
        else:
            lp = (
                0.4648 * cage
                + 0.7744 * smoking
                + 0.3131 * csbp
                + 0.1002 * ctchol
                - 0.2606 * chdl
                - 0.1088 * cage * smoking
                - 0.0277 * cage * csbp
                - 0.0226 * cage * ctchol
                + 0.0613 * cage * chdl
            )

        # Uncalibrated risk: 1 - S0 ^ exp(lp)
        s0 = _S0[sex]
        exp_lp = math.exp(lp)
        uncalibrated_surv = math.pow(s0, exp_lp)
        uncalibrated_risk = max(1e-7, min(1.0 - 1e-7, 1.0 - uncalibrated_surv))

        # Regional recalibration:
        # 1 - exp(-exp(scale1 + scale2 * ln(-ln(1 - uncalibrated_risk))))
        scale1, scale2 = _REGIONAL_SCALES[region][sex]
        inner_log = math.log(-math.log(1.0 - uncalibrated_risk))
        calibrated_exponent = scale1 + scale2 * inner_log
        calibrated_risk = 1.0 - math.exp(-math.exp(calibrated_exponent))
        calibrated_risk = max(0.0, min(1.0, calibrated_risk))

        raw_value = round(calibrated_risk * 100.0, 1)

        # Normalized value (0 to 100, where 0 is lowest risk, 100 is max risk)
        risk_value = round(
            max(
                0.0,
                min(100.0, (raw_value / _NORMALIZATION_RISK_CEILING_PERCENT) * 100.0),
            ),
            1,
        )

        if raw_value < 5.0:
            risk_level = "Low risk"
        elif raw_value < 10.0:
            risk_level = "Moderate risk"
        elif raw_value < 20.0:
            risk_level = "High risk"
        else:
            risk_level = "Very high risk"

        attention_flags = {
            "high_cardiovascular_risk": raw_value >= 10.0,
            "smoker": bool(data.smoker),
            "elevated_blood_pressure": float(data.systolic_blood_pressure) >= 140.0,
        }

        contributing_factors = {
            "age": float(data.age),
            "smoker": smoking,
            "systolic_blood_pressure": float(data.systolic_blood_pressure),
            "total_cholesterol_mmol": round(total_chol_mmol, 2),
            "hdl_cholesterol_mmol": round(hdl_chol_mmol, 2),
            "linear_predictor": round(lp, 4),
            "uncalibrated_risk_percent": round(uncalibrated_risk * 100.0, 2),
            "calibrated_risk_percent": raw_value,
        }

        explanation = (
            f"Estimated 10-year risk of fatal and non-fatal cardiovascular "
            f"disease event is {raw_value}% ({risk_level})."
        )

        return ScoreResult(
            score_id="score2",
            score_name="SCORE2",
            domain="Cardiovascular",
            status=CalculationStatus.CALCULATED,
            raw_value=raw_value,
            risk_value=risk_value,
            risk_level=risk_level,
            explanation=explanation,
            contributing_factors=contributing_factors,
            attention_flags=attention_flags,
        )
