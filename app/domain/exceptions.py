"""Domain exceptions for the Engine."""

from __future__ import annotations


class EngineDomainError(Exception):
    """Base exception for all domain errors."""


class InvalidHealthDataError(EngineDomainError):
    """Raised when the provided health data violates basic business rules."""


class ScoreCalculatorNotFoundError(EngineDomainError):
    """Raised when a requested score calculator is not found."""
