"""Domain entity for PHQ-9 (depression screening) data."""

from __future__ import annotations

from dataclasses import dataclass

PHQ9_ITEM_FIELDS: tuple[str, ...] = (
    "little_interest",
    "feeling_down",
    "sleep_trouble",
    "tired_energy",
    "appetite",
    "feeling_bad",
    "concentration",
    "psychomotor",
    "self_harm_thoughts",
)


@dataclass(frozen=True)
class Phq9Data:
    """Nine PHQ-9 item responses for the previous two weeks, each scored 0–3."""

    little_interest: int | None = None
    feeling_down: int | None = None
    sleep_trouble: int | None = None
    tired_energy: int | None = None
    appetite: int | None = None
    feeling_bad: int | None = None
    concentration: int | None = None
    psychomotor: int | None = None
    self_harm_thoughts: int | None = None
