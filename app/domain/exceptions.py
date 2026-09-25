"""Domain exceptions for the Engine."""

from __future__ import annotations


class EngineDomainError(Exception):
    """Base exception for all domain errors."""


class ScoreCalculatorNotFoundError(EngineDomainError):
    """Raised when a requested score calculator is not found."""
