"""Domain models for employee health data."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EmployeeHealthData:
    """
    Represents the health parameters provided by the client.
    All fields are optional because different calculators require different data.
    Each calculator is responsible for validating if it has the required fields.
    """

    age: int | None = None
    sex: str | None = None
    weight: float | None = None
    height: float | None = None
    waist_circumference: float | None = None
    systolic_blood_pressure: float | None = None
    total_cholesterol: float | None = None
    hdl: float | None = None
    triglycerides: float | None = None
    smoker: bool | None = None
    daily_physical_activity: bool | None = None
    fruits_vegetables: bool | None = None
    hypertension_medication: bool | None = None
    previous_high_glucose: bool | None = None
    family_diabetes: str | None = None
    snoring: bool | None = None
    tired: bool | None = None
    observed_apnea: bool | None = None
    neck_circumference: float | None = None
