# kernel/container/scopes.py
"""
Lifetime scopes for the CAMEAL Kernel Container.

Defines the possible lifetimes for registered dependencies:
- SINGLETON: One instance for the lifetime of the container.
- REQUEST: One instance per execution request.
- TRANSIENT: A new instance created on every resolution.
"""

from enum import Enum


class Scope(str, Enum):
    """
    Lifetime scope for a dependency.

    The scope determines when a new instance is created and how long it is cached.

    Examples:
        >>> Scope.SINGLETON
        <Scope.SINGLETON: 'singleton'>
        >>> Scope.REQUEST
        <Scope.REQUEST: 'request'>
        >>> Scope.TRANSIENT
        <Scope.TRANSIENT: 'transient'>
    """

    SINGLETON = "singleton"
    REQUEST = "request"
    TRANSIENT = "transient"

    def __str__(self) -> str:
        return self.value

    @property
    def is_singleton(self) -> bool:
        """Return True if this scope is SINGLETON."""
        return self == Scope.SINGLETON

    @property
    def is_request(self) -> bool:
        """Return True if this scope is REQUEST."""
        return self == Scope.REQUEST

    @property
    def is_transient(self) -> bool:
        """Return True if this scope is TRANSIENT."""
        return self == Scope.TRANSIENT
