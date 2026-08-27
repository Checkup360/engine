"""Registry for score-specific request models."""

from __future__ import annotations

from typing import Any, Protocol

from pydantic import BaseModel

from app.presentation.api.request_models.scores.findrisc_request import (
    FindriscRequest,
)
from app.presentation.api.request_models.scores.stop_bang_request import (
    StopBangRequest,
)


class ScoreRequestProtocol(Protocol):
    def to_domain(self) -> Any: ...


SCORE_REQUEST_REGISTRY: dict[str, type[BaseModel]] = {
    "findrisc": FindriscRequest,
    "stop_bang": StopBangRequest,
}


def get_request_model(score_id: str) -> type[BaseModel] | None:
    """Returns the request model class registered for score_id, or None."""
    return SCORE_REQUEST_REGISTRY.get(score_id)
