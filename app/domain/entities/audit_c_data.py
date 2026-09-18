"""Domain entity for AUDIT-C alcohol consumption risk data."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AuditCData:
    """Clinical parameters required to compute the AUDIT-C alcohol risk score."""

    frequency: int | None = None
    quantity: int | None = None
    heavy_drinking: int | None = None
    sex: str | None = None
