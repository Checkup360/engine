"""HTTP request model for EOSS."""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.domain.entities.eoss_data import EOSSData


class EOSSRequest(BaseModel):
    """Clinician-assessed EOSS stage for each health domain."""

    physical_health_stage: int = Field(..., ge=0, le=4)
    mental_health_stage: int = Field(..., ge=0, le=4)
    functional_stage: int = Field(..., ge=0, le=4)

    def to_domain(self) -> EOSSData:
        """Converts the HTTP request model into its domain entity."""
        return EOSSData(**self.model_dump())
