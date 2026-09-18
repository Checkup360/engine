"""HTTP request model for AUDIT-C score."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from app.domain.entities.audit_c_data import AuditCData


class AuditCRequest(BaseModel):
    """Payload for AUDIT-C alcohol risk calculation."""

    frequency: int = Field(..., ge=0, le=4, description="Frequency of alcohol consumption (0-4)")
    quantity: int = Field(..., ge=0, le=4, description="Quantity of drinks on typical day (0-4)")
    heavy_drinking: int = Field(..., ge=0, le=4, description="Frequency of 6+ drinks on one occasion (0-4)")
    sex: Literal["M", "F", "m", "f"] = Field(..., description="Biological sex ('M' or 'F')")

    def to_domain(self) -> AuditCData:
        return AuditCData(
            frequency=self.frequency,
            quantity=self.quantity,
            heavy_drinking=self.heavy_drinking,
            sex=self.sex.upper(),
        )
