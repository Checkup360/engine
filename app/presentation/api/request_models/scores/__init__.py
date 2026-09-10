"""Score Request Models."""

from app.presentation.api.request_models.scores.findrisc_request import (
    FindriscRequest,
)
from app.presentation.api.request_models.scores.phq9_request import Phq9Request
from app.presentation.api.request_models.scores.stop_bang_request import (
    StopBangRequest,
)

__all__ = [
    "FindriscRequest",
    "Phq9Request",
    "StopBangRequest",
]
