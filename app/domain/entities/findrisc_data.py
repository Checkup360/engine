"""Domain entity for FINDRISC (Diabetes Risk) data."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FindriscData:
    """Clinical parameters required to compute the FINDRISC score."""

    age: int | None = None
    sex: str | None = None
    weight: float | None = None
    height: float | None = None
    waist_circumference: float | None = None
    daily_physical_activity: bool | None = None
    fruits_vegetables: bool | None = None
    hypertension_medication: bool | None = None
    previous_high_glucose: bool | None = None
    family_diabetes: str | None = None
