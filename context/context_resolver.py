"""
===============================================================================
Module: context.context_resolver

Governance Context Resolver.

Resolves GovernanceContext objects from a read‑only registry.

The resolver never creates or modifies contexts – only retrieves them.
===============================================================================
"""

from __future__ import annotations

from .context import GovernanceContext
from .context_registry import ReadOnlyContextRegistry, ContextRegistry


class ContextResolver:
    """
    Resolves governance contexts from a read‑only registry.
    """

    def __init__(self, registry: ReadOnlyContextRegistry | ContextRegistry) -> None:
        # If a mutable registry is passed, we only use its read methods.
        self._registry = registry

    @property
    def registry(self) -> ReadOnlyContextRegistry | ContextRegistry:
        """Read‑only access to the underlying registry."""
        return self._registry

    def resolve(self, identifier: str) -> GovernanceContext:
        context = self._registry.get(identifier)
        if context is None:
            raise KeyError(f"Unknown context '{identifier}'.")
        return context

    def resolve_many(self, identifiers: tuple[str, ...]) -> tuple[GovernanceContext, ...]:
        return tuple(self.resolve(identifier) for identifier in identifiers)

    def exists(self, identifier: str) -> bool:
        return self._registry.contains(identifier)
