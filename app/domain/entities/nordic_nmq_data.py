"""Domain entity for Standardized Nordic Questionnaire (NMQ) Ergonomic Risk data."""

from __future__ import annotations

from dataclasses import dataclass, field

NMQ_ANATOMICAL_ZONES = [
    "neck",
    "shoulders",
    "upper_back",
    "lower_back",
    "elbows",
    "wrists_hands",
    "hips_thighs",
    "knees",
    "ankles_feet",
]


@dataclass(frozen=True)
class ZoneNmqData:
    """NMQ responses for a single anatomical body zone."""

    trouble_last_12_months: bool | None = None
    prevented_work_last_12_months: bool | None = None
    trouble_last_7_days: bool | None = None


@dataclass(frozen=True)
class NordicNmqData:
    """Clinical ergonomic parameters required to compute the NMQ score."""

    zones: dict[str, ZoneNmqData] = field(default_factory=dict)
