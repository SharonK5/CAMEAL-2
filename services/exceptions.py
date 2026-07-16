"""
===============================================================================
Module: services.exceptions

Service subsystem exceptions.
===============================================================================
"""

from __future__ import annotations


class ServiceError(Exception):
    """Base exception for service subsystem."""


class DuplicateServiceError(ServiceError):
    """Raised when attempting to register a service with a duplicate name."""
