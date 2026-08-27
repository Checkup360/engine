"""HTTP request model for FINDRISC score."""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.domain.entities.findrisc_data import FindriscData


class FindriscRequest(BaseModel):
    """Payload for FINDRISC diabetes risk calculation."""

    age: int | None = Field(None, ge=0, le=130, description="Age in years")
    sex: str | None = Field(None, description="Biological sex ('M' or 'F')")
    weight: float | None = Field(None, gt=0, lt=500, description="Weight in kilograms")
    height: float | None = Field(None, gt=0, lt=3.0, description="Height in meters")
    waist_circumference: float | None = Field(
        None, gt=0, lt=300, description="Waist circumference in cm"
    )
    daily_physical_activity: bool | None = Field(
        None, description="At least 30 min of daily physical activity"
    )
    fruits_vegetables: bool | None = Field(
        None, description="Eats fruits or vegetables daily"
    )
    hypertension_medication: bool | None = Field(
        None, description="Regularly takes medication for high blood pressure"
    )
    previous_high_glucose: bool | None = Field(
        None, description="Ever found to have high blood glucose"
    )
    family_diabetes: str | None = Field(
        None,
        description=(
            "Family history of diabetes ('none', 'second_degree', 'first_degree')"
        ),
    )

    def to_domain(self) -> FindriscData:
        """Converts HTTP request model directly into domain FindriscData entity."""
        return FindriscData(**self.model_dump())
