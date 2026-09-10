"""HTTP request model for metabolic syndrome criteria."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from app.domain.entities.metabolic_syndrome_data import MetabolicSyndromeData


class MetabolicSyndromeRequest(BaseModel):
    """Payload for calculating the five metabolic syndrome criteria."""

    sex: Literal["M", "F"] = Field(..., description="Biological sex ('M' or 'F')")
    waist_circumference: float = Field(..., gt=0, lt=300, description="Waist in cm")
    triglycerides: float = Field(
        ..., ge=0, lt=10000, description="Triglycerides in mg/dL"
    )
    hdl_cholesterol: float = Field(
        ..., ge=0, lt=1000, description="HDL cholesterol in mg/dL"
    )
    systolic_blood_pressure: float = Field(
        ..., gt=0, lt=400, description="Systolic blood pressure in mmHg"
    )
    diastolic_blood_pressure: float = Field(
        ..., gt=0, lt=300, description="Diastolic blood pressure in mmHg"
    )
    hypertension_medication: bool = Field(
        ..., description="Taking antihypertensive medication"
    )
    fasting_glucose: float = Field(
        ..., ge=0, lt=2000, description="Fasting glucose in mg/dL"
    )
    glucose_lowering_medication: bool = Field(
        ..., description="Taking glucose-lowering medication"
    )

    def to_domain(self) -> MetabolicSyndromeData:
        """Converts the HTTP request model into its domain entity."""
        return MetabolicSyndromeData(**self.model_dump())
