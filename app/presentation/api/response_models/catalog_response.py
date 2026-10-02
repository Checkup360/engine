"""Response models for risk score catalog endpoint."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ScoreCatalogItemResponse(BaseModel):
    """Schema representing an available risk score and its required/optional fields."""

    score_id: str
    score_name: str
    domain: str
    topic_key: str = Field(
        description="Stable key of the health topic, used for weights and content."
    )
    topic_label: str = Field(description="Readable name of the health topic.")
    required_fields: list[str]
    optional_fields: list[str]
    field_schema: dict[str, Any]
