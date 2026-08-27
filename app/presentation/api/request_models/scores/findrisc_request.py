"""HTTP request model for FINDRISC score."""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.domain.entities.findrisc_data import FindriscData


class FindriscRequest(BaseModel):
    """Payload for FINDRISC diabetes risk calculation."""

    age: int = Field(..., ge=0, le=130, description="Age in years")
    sex: str = Field(..., description="Biological sex ('M' or 'F')")
    weight: float = Field(..., gt=0, lt=500, description="Weight in kilograms")
    height: float = Field(..., gt=0, lt=3.0, description="Height in meters")
    waist_circumference: float = Field(
        ..., gt=0, lt=300, description="Waist circumference in cm"
    )
    daily_physical_activity: bool = Field(
        ..., description="At least 30 min of daily physical activity"
    )
    fruits_vegetables: bool = Field(..., description="Eats fruits or vegetables daily")
    hypertension_medication: bool = Field(
        ..., description="Regularly takes medication for high blood pressure"
    )
    previous_high_glucose: bool = Field(
        ..., description="Ever found to have high blood glucose"
    )
    family_diabetes: str = Field(
        ...,
        description=(
            "Family history of diabetes ('no', 'second_degree', 'first_degree')"
        ),
    )

    def to_domain(self) -> FindriscData:
        """Converts HTTP request model directly into domain FindriscData entity."""
        return FindriscData(**self.model_dump())
