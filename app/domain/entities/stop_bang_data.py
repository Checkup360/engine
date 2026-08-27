"""Domain entity for STOP-BANG (Sleep Apnea Screening) data."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StopBangData:
    """Clinical parameters required to compute the STOP-BANG score."""

    snoring: bool | None = None
    tired: bool | None = None
    observed_apnea: bool | None = None
    hypertension_medication: bool | None = None
    weight: float | None = None
    height: float | None = None
    age: int | None = None
    neck_circumference: float | None = None
    sex: str | None = None
