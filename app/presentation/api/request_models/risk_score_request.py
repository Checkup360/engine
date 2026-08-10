"""HTTP request models for the risk scoring API."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class RiskScoreRequest(BaseModel):
    """
    Validates the JSON body sent by the client.
    All fields are optional, calculators will decide if they have enough data.
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
