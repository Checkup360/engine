"""Score Request Models."""

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

__all__ = [
    "FindriscRequest",
    "EOSSRequest",
    "MetabolicSyndromeRequest",
    "Phq9Request",
    "Score2Request",
    "StopBangRequest",
    "NordicNmqRequest",
    "AuditCRequest",
    "Pss10Request",
]
