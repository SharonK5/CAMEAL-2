# kernel/context/exceptions.py
"""
Context-specific exceptions.
"""


class ContextError(Exception):
    """Base exception for all context-related errors."""


class ContextValidationError(ContextError):
    """Raised when context validation fails."""


class ContextBuilderError(ContextError):
    """Raised when context building fails."""


class ContextNotFoundError(ContextError):
    """Raised when a requested context type is not found."""


class ContextRegistryError(ContextError):
    """Raised when context registry operations fail."""	
