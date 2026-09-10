"""Domain entity for Edmonton Obesity Staging System data."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EOSSData:
    """Clinician-assessed severity across EOSS health domains."""

    physical_health_stage: int | None = None
    mental_health_stage: int | None = None
    functional_stage: int | None = None