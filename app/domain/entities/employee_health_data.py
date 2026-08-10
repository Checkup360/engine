"""Domain models for employee health data."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class EmployeeHealthData:
    """
    Represents the health parameters provided by the client.
    All fields are optional because different calculators require different data.
    Each calculator is responsible for validating if it has the required fields.
    """

    age: Optional[int] = None
    sex: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    waist_circumference: Optional[float] = None
    systolic_blood_pressure: Optional[float] = None
    total_cholesterol: Optional[float] = None
    hdl: Optional[float] = None
    triglycerides: Optional[float] = None
    smoker: Optional[bool] = None
    daily_physical_activity: Optional[bool] = None
    fruits_vegetables: Optional[bool] = None
    hypertension_medication: Optional[bool] = None
    previous_high_glucose: Optional[bool] = None
    family_diabetes: Optional[str] = None
    snoring: Optional[bool] = None
    tired: Optional[bool] = None
    observed_apnea: Optional[bool] = None
    neck_circumference: Optional[float] = None
