"""Domain entity for PSS-10 Perceived Stress Scale data."""

from __future__ import annotations

from dataclasses import dataclass

PSS10_REVERSED_ITEMS = {"pss10_q4", "pss10_q5", "pss10_q7", "pss10_q8"}
PSS10_ALL_FIELDS = [f"pss10_q{i}" for i in range(1, 11)]


@dataclass(frozen=True)
class Pss10Data:
    """Psychological parameters required to compute the PSS-10 stress score."""

    pss10_q1: int | None = None
    pss10_q2: int | None = None
    pss10_q3: int | None = None
    pss10_q4: int | None = None
    pss10_q5: int | None = None
    pss10_q6: int | None = None
    pss10_q7: int | None = None
    pss10_q8: int | None = None
    pss10_q9: int | None = None
    pss10_q10: int | None = None
