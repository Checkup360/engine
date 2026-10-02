"""Value object for the health topic a risk score belongs to."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HealthTopic:
    """
    Health topic covered by a score, shared by every consumer of scores.

    ``key`` is the stable identifier organizations use to weight and enable
    scores and that content is tagged with. ``label`` is its readable name.
    """

    key: str
    label: str

    def __post_init__(self) -> None:
        if not self.key.strip() or not self.label.strip():
            raise ValueError("HealthTopic key and label must not be empty")
