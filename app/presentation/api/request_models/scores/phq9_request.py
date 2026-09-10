"""HTTP request model for PHQ-9 score."""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.domain.entities.phq9_data import Phq9Data

_ITEM_DESCRIPTION = (
    "How often the symptom bothered you over the last 2 weeks: "
    "0 = not at all, 1 = several days, 2 = more than half the days, "
    "3 = nearly every day"
)


class Phq9Request(BaseModel):
    """Payload for PHQ-9 depression screening."""

    little_interest: int = Field(..., ge=0, le=3, description=_ITEM_DESCRIPTION)
    feeling_down: int = Field(..., ge=0, le=3, description=_ITEM_DESCRIPTION)
    sleep_trouble: int = Field(..., ge=0, le=3, description=_ITEM_DESCRIPTION)
    tired_energy: int = Field(..., ge=0, le=3, description=_ITEM_DESCRIPTION)
    appetite: int = Field(..., ge=0, le=3, description=_ITEM_DESCRIPTION)
    feeling_bad: int = Field(..., ge=0, le=3, description=_ITEM_DESCRIPTION)
    concentration: int = Field(..., ge=0, le=3, description=_ITEM_DESCRIPTION)
    psychomotor: int = Field(..., ge=0, le=3, description=_ITEM_DESCRIPTION)
    self_harm_thoughts: int = Field(..., ge=0, le=3, description=_ITEM_DESCRIPTION)

    def to_domain(self) -> Phq9Data:
        """Converts HTTP request model directly into domain Phq9Data entity."""
        return Phq9Data(**self.model_dump())
