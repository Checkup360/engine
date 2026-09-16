"""HTTP request model for PSS-10 score."""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.domain.entities.pss10_data import Pss10Data


class Pss10Request(BaseModel):
    """Payload for PSS-10 perceived stress scale calculation."""

    pss10_q1: int = Field(..., ge=0, le=4, description="Question 1 (0-4)")
    pss10_q2: int = Field(..., ge=0, le=4, description="Question 2 (0-4)")
    pss10_q3: int = Field(..., ge=0, le=4, description="Question 3 (0-4)")
    pss10_q4: int = Field(..., ge=0, le=4, description="Question 4 (0-4, reversed)")
    pss10_q5: int = Field(..., ge=0, le=4, description="Question 5 (0-4, reversed)")
    pss10_q6: int = Field(..., ge=0, le=4, description="Question 6 (0-4)")
    pss10_q7: int = Field(..., ge=0, le=4, description="Question 7 (0-4, reversed)")
    pss10_q8: int = Field(..., ge=0, le=4, description="Question 8 (0-4, reversed)")
    pss10_q9: int = Field(..., ge=0, le=4, description="Question 9 (0-4)")
    pss10_q10: int = Field(..., ge=0, le=4, description="Question 10 (0-4)")

    def to_domain(self) -> Pss10Data:
        return Pss10Data(**self.model_dump())
