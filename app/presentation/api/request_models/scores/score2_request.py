"""HTTP request model for SCORE2 cardiovascular risk."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from app.domain.entities.score2_data import Score2Data


class Score2Request(BaseModel):
    """Payload for calculating SCORE2 cardiovascular risk."""

    age: int = Field(..., ge=18, le=120, description="Age in years")
    sex: Literal["M", "F"] = Field(..., description="Biological sex ('M' or 'F')")
    smoker: bool = Field(..., description="Current smoking status")
    systolic_blood_pressure: float = Field(
        ..., gt=0, lt=400, description="Systolic blood pressure in mmHg"
    )
    total_cholesterol: float = Field(
        ..., gt=0, lt=1000, description="Total cholesterol in mmol/L or mg/dL"
    )
    hdl_cholesterol: float = Field(
        ..., gt=0, lt=500, description="HDL cholesterol in mmol/L or mg/dL"
    )
    risk_region: Literal["low", "moderate", "high", "very_high"] = Field(
        default="moderate", description="European risk region"
    )

    def to_domain(self) -> Score2Data:
        """Converts the HTTP request model into its domain entity."""
        return Score2Data(**self.model_dump())
