"""Registry for score-specific request models and catalog discovery."""

from __future__ import annotations

from typing import Any, Protocol

from pydantic import BaseModel

from app.presentation.api.request_models.scores.eoss_request import EOSSRequest
from app.presentation.api.request_models.scores.findrisc_request import (
    FindriscRequest,
)
from app.presentation.api.request_models.scores.metabolic_syndrome_request import (
    MetabolicSyndromeRequest,
)
from app.presentation.api.request_models.scores.phq9_request import Phq9Request
from app.presentation.api.request_models.scores.stop_bang_request import (
    StopBangRequest,
)
from app.presentation.api.response_models.catalog_response import (
    ScoreCatalogItemResponse,
)


class ScoreRequestProtocol(Protocol):
    def to_domain(self) -> Any: ...


SCORE_REQUEST_REGISTRY: dict[str, type[BaseModel]] = {
    "findrisc": FindriscRequest,
    "eoss": EOSSRequest,
    "metabolic_syndrome": MetabolicSyndromeRequest,
    "stop_bang": StopBangRequest,
    "phq9": Phq9Request,
}

SCORE_METADATA_REGISTRY: dict[str, dict[str, str]] = {
    "findrisc": {"score_name": "FINDRISC", "domain": "Diabetes"},
    "eoss": {
        "score_name": "EOSS",
        "domain": "Obesity-related Health Impact",
    },
    "metabolic_syndrome": {
        "score_name": "Metabolic Syndrome",
        "domain": "Metabolic Health",
    },
    "stop_bang": {"score_name": "STOP-BANG", "domain": "Sleep Apnea"},
    "phq9": {"score_name": "PHQ-9", "domain": "Depression"},
}


def get_request_model(score_id: str) -> type[BaseModel] | None:
    """Returns the request model class registered for score_id, or None."""
    return SCORE_REQUEST_REGISTRY.get(score_id)


def get_catalog() -> list[ScoreCatalogItemResponse]:
    """Dynamically generates the catalog of all registered score calculators."""
    catalog: list[ScoreCatalogItemResponse] = []
    for score_id, model_cls in SCORE_REQUEST_REGISTRY.items():
        meta = SCORE_METADATA_REGISTRY.get(
            score_id, {"score_name": score_id.upper(), "domain": "General"}
        )
        required_fields: list[str] = []
        optional_fields: list[str] = []

        for field_name, field_info in model_cls.model_fields.items():
            if field_info.is_required():
                required_fields.append(field_name)
            else:
                optional_fields.append(field_name)

        catalog.append(
            ScoreCatalogItemResponse(
                score_id=score_id,
                score_name=meta["score_name"],
                domain=meta["domain"],
                required_fields=required_fields,
                optional_fields=optional_fields,
                field_schema=model_cls.model_json_schema(),
            )
        )
    return catalog
