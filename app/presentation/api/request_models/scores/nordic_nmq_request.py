"""HTTP request model for Standardized Nordic Questionnaire (NMQ) score."""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.domain.entities.nordic_nmq_data import NordicNmqData, ZoneNmqData


class ZoneNmqRequest(BaseModel):
    """Payload for a single anatomical body zone in NMQ."""

    trouble_last_12_months: bool = Field(
        ..., description="Trouble/pain in last 12 months"
    )
    prevented_work_last_12_months: bool = Field(
        ..., description="Prevented normal work in last 12 months"
    )
    trouble_last_7_days: bool = Field(..., description="Trouble/pain in last 7 days")

    def to_domain(self) -> ZoneNmqData:
        return ZoneNmqData(**self.model_dump())


class NordicNmqRequest(BaseModel):
    """Payload for Standardized Nordic Questionnaire ergonomic risk calculation."""

    zones: dict[str, ZoneNmqRequest] = Field(
        ..., description="Map of 9 anatomical zones to NMQ responses"
    )

    def to_domain(self) -> NordicNmqData:
        domain_zones = {k: ZoneNmqData(**v.model_dump()) for k, v in self.zones.items()}
        return NordicNmqData(zones=domain_zones)
