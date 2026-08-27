"""Response models for risk score catalog endpoint."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class ScoreCatalogItemResponse(BaseModel):
    """Schema representing an available risk score and its required/optional fields."""

    score_id: str
    score_name: str
    domain: str
    required_fields: list[str]
    optional_fields: list[str]
    field_schema: dict[str, Any]
