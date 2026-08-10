"""HTTP request models for the risk scoring API."""

from __future__ import annotations

from pydantic import BaseModel


class RiskScoreRequest(BaseModel):
    """
    Validates the JSON body sent by the client.
    All fields are optional, calculators will decide if they have enough data.
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
