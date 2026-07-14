"""
===============================================================================
Module: context.context_resolver

Governance Context Resolver.

Resolves GovernanceContext objects from registered context dimensions.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from .context import GovernanceContext
from .context_registry import ContextRegistry


class ContextResolver:
    """
    Resolves governance contexts from the registry.

    The resolver never creates governance objects directly.
    It only retrieves and combines registered objects.

    The registry is exposed as a read‑only property for inspection.
    """

    def __init__(
        self,
        registry: ContextRegistry,
    ) -> None:
        self._registry = registry

    @property
    def registry(self) -> ContextRegistry:
        """
        Read‑only access to the underlying registry.
        Useful for diagnostics, monitoring, and testing.
        """
        return self._registry

    def resolve(
        self,
        identifier: str,
    ) -> GovernanceContext:
        """
        Resolve a single GovernanceContext.

        Raises
        ------
        KeyError
            If the context does not exist.
        """
        context = self._registry.get(identifier)
        if context is None:
            raise KeyError(f"Unknown context '{identifier}'.")
        return context

    def resolve_many(
        self,
        identifiers: tuple[str, ...],
    ) -> tuple[GovernanceContext, ...]:
        """
        Resolve multiple governance contexts in one call.

        Useful for the Query Engine when multiple dimensions
        (institution, jurisdiction, spatial region, time period)
        need to be resolved together.
        """
        return tuple(self.resolve(identifier) for identifier in identifiers)

    def exists(
        self,
        identifier: str,
    ) -> bool:
        """Check if a context exists by identifier."""
        return self._registry.contains(identifier)
