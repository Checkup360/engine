"""Domain entity for SCORE2 cardiovascular risk data."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Score2Data:
    """Inputs required for SCORE2 10-year fatal and non-fatal CVD risk calculation."""

    age: int | None = None
    sex: str | None = None  # "M" or "F"
    smoker: bool | None = None
    systolic_blood_pressure: float | None = None
    total_cholesterol: float | None = None  # mmol/L or mg/dL (auto-converted)
    hdl_cholesterol: float | None = None  # mmol/L or mg/dL (auto-converted)
    risk_region: str = "moderate"  # "low", "moderate", "high", or "very_high"
