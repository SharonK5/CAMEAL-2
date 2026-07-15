"""
===============================================================================
Module: context.exceptions

Custom exceptions for the context subsystem.
===============================================================================
"""


class ContextError(Exception):
    """Base exception for the context subsystem."""
    pass


class ContextNotFoundError(ContextError):
    """Raised when a context is not found in the registry."""
    pass


class CircularParentError(ContextError):
    """Raised when a circular parent relationship is detected."""
    pass


class InvalidContextDataError(ContextError):
    """Raised when context data fails validation (e.g., invalid schema)."""
    pass
