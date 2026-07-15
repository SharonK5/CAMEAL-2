"""
===============================================================================
Module: context.context_loader

Orchestrates loading contexts from one or more providers.
===============================================================================
"""

from __future__ import annotations

from typing import Sequence, Optional

from .context import GovernanceContext
from .context_provider import ContextProvider


class ContextLoader:
    """
    Loads contexts from a chain of providers (first match wins).
    """

    def __init__(self, providers: Sequence[ContextProvider]) -> None:
        self._providers = providers

    def get(self, identifier: str) -> GovernanceContext | None:
        for provider in self._providers:
            context = provider.get(identifier)
            if context is not None:
                return context
        return None

    def load_all(self) -> Sequence[GovernanceContext]:
        # Collect from all providers, deduplicate by identifier
        seen: set[str] = set()
        result: list[GovernanceContext] = []
        for provider in self._providers:
            for ctx in provider.load_all():
                inst = ctx.institutional
                if inst and inst.identifier not in seen:
                    seen.add(inst.identifier)
                    result.append(ctx)
        return tuple(result)
