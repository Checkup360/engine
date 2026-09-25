"""Shared validation types and helpers for score request models."""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BeforeValidator, Field


def _normalize_sex(v: object) -> object:
    if isinstance(v, str):
        val = v.upper()
        if val in ("M", "F"):
            return val
    return v


Sex = Annotated[
    Literal["M", "F"],
    BeforeValidator(_normalize_sex),
    Field(description="Biological sex ('M' or 'F')"),
]
