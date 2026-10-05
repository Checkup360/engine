"""Registry for score-specific request models and catalog discovery."""

from __future__ import annotations

from typing import Any, Protocol

from pydantic import BaseModel

from app.domain.value_objects.health_topic import HealthTopic
from app.presentation.api.request_models.scores.audit_c_request import AuditCRequest
from app.presentation.api.request_models.scores.eoss_request import EOSSRequest
from app.presentation.api.request_models.scores.findrisc_request import (
    FindriscRequest,
)
from app.presentation.api.request_models.scores.metabolic_syndrome_request import (
    MetabolicSyndromeRequest,
)
from app.presentation.api.request_models.scores.nordic_nmq_request import (
    NordicNmqRequest,
)
from app.presentation.api.request_models.scores.phq9_request import Phq9Request
from app.presentation.api.request_models.scores.pss10_request import Pss10Request
from app.presentation.api.request_models.scores.score2_request import Score2Request
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
    "score2": Score2Request,
    "nordic_nmq": NordicNmqRequest,
    "audit_c": AuditCRequest,
    "pss10": Pss10Request,
}

SCORE_METADATA_REGISTRY: dict[str, dict[str, str]] = {
    "findrisc": {"score_name": "FINDRISC", "domain": "Diabetes"},
    "eoss": {
        "score_name": "EOSS",
        "domain": "Obesity Impact",
    },
    "metabolic_syndrome": {
        "score_name": "Metabolic Syndrome",
        "domain": "Metabolic Health",
    },
    "stop_bang": {"score_name": "STOP-BANG", "domain": "Sleep Apnea"},
    "phq9": {"score_name": "PHQ-9", "domain": "Mood & Well-being"},
    "score2": {"score_name": "SCORE2", "domain": "Cardiovascular"},
    "nordic_nmq": {
        "score_name": "Standardized Nordic Questionnaire (NMQ)",
        "domain": "Musculoskeletal",
    },
    "audit_c": {"score_name": "AUDIT-C Alcohol Risk", "domain": "Alcohol Habits"},
    "pss10": {
        "score_name": "PSS-10 Perceived Stress Scale",
        "domain": "Stress & Burnout",
    },
}


def get_request_model(score_id: str) -> type[BaseModel] | None:
    """Returns the request model class registered for score_id, or None."""
    return SCORE_REQUEST_REGISTRY.get(score_id)


def get_catalog(
    topics_by_score: dict[str, HealthTopic],
) -> list[ScoreCatalogItemResponse]:
    """Dynamically generates the catalog of all registered score calculators."""
    catalog: list[ScoreCatalogItemResponse] = []
    for score_id, model_cls in SCORE_REQUEST_REGISTRY.items():
        topic = topics_by_score.get(score_id)
        if topic is None:
            continue
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
                topic_key=topic.key,
                topic_label=topic.label,
                required_fields=required_fields,
                optional_fields=optional_fields,
                field_schema=model_cls.model_json_schema(),
            )
        )
    return catalog
