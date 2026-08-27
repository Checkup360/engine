"""HTTP request model for STOP-BANG score."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from app.domain.entities.stop_bang_data import StopBangData


class StopBangRequest(BaseModel):
    """Payload for STOP-BANG sleep apnea screening."""

    snoring: bool = Field(..., description="Do you snore loudly (louder than talking)?")
    tired: bool = Field(
        ...,
        description="Do you often feel tired, fatigued, or sleepy during daytime?",
    )
    observed_apnea: bool = Field(
        ..., description="Has anyone observed you stop breathing during sleep?"
    )
    hypertension_medication: bool = Field(
        ...,
        description="Do you have or are being treated for high blood pressure?",
    )
    weight: float = Field(..., gt=0, lt=500, description="Weight in kilograms")
    height: float = Field(..., gt=0, lt=3.0, description="Height in meters")
    age: int = Field(..., ge=0, le=130, description="Age in years")
    neck_circumference: float = Field(
        ..., gt=0, lt=100, description="Neck circumference in cm"
    )
    sex: Literal["M", "F"] = Field(..., description="Biological sex ('M' or 'F')")

    def to_domain(self) -> StopBangData:
        """Converts HTTP request model directly into domain StopBangData entity."""
        return StopBangData(**self.model_dump())
