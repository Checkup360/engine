"""Domain entities."""

from app.domain.entities.eoss_data import EOSSData
from app.domain.entities.findrisc_data import FindriscData
from app.domain.entities.metabolic_syndrome_data import MetabolicSyndromeData
from app.domain.entities.phq9_data import Phq9Data
from app.domain.entities.stop_bang_data import StopBangData

__all__ = [
    "FindriscData",
    "EOSSData",
    "MetabolicSyndromeData",
    "Phq9Data",
    "StopBangData",
]
