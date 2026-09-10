"""Domain entity for metabolic syndrome criteria data."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MetabolicSyndromeData:
    """Measurements and treatment indicators for the five AHA criteria."""

    sex: str | None = None
    waist_circumference: float | None = None
    triglycerides: float | None = None
    hdl_cholesterol: float | None = None
    systolic_blood_pressure: float | None = None
    diastolic_blood_pressure: float | None = None
    hypertension_medication: bool | None = None
    fasting_glucose: float | None = None
    glucose_lowering_medication: bool | None = None
