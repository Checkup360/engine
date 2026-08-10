"""Domain exceptions for the Motor."""

from __future__ import annotations


class MotorDomainError(Exception):
    """Base exception for all domain errors."""


class InvalidHealthDataError(MotorDomainError):
    """Raised when the provided health data violates basic business rules."""
