"""
===============================================================================
Module: context.context_cache

In‑memory cache for GovernanceContext objects.
===============================================================================
"""

from __future__ import annotations

import time
from typing import Sequence, Optional

from .context import GovernanceContext
from .context_provider import ContextProvider


class CachedContextProvider(ContextProvider):
    """
    Wraps another provider with an in‑memory cache.
    """

    def __init__(self, provider: ContextProvider, ttl_seconds: int = 60) -> None:
        self._provider = provider
        self._ttl = ttl_seconds
        self._cache: dict[str, tuple[float, GovernanceContext]] = {}
        self._all_cached: tuple[float, Sequence[GovernanceContext]] | None = None
        self._all_identifiers_cached: tuple[float, Sequence[str]] | None = None

    def _is_expired(self, timestamp: float) -> bool:
        return time.monotonic() - timestamp > self._ttl

    def _get_or_load(self, identifier: str) -> GovernanceContext | None:
        now = time.monotonic()
        cached = self._cache.get(identifier)
        if cached and not self._is_expired(cached[0]):
            return cached[1]

        # Load from underlying provider
        context = self._provider.get(identifier)
        if context is not None:
            self._cache[identifier] = (now, context)
        return context

    def get(self, identifier: str) -> GovernanceContext | None:
        return self._get_or_load(identifier)

    def list_identifiers(self) -> Sequence[str]:
        now = time.monotonic()
        if self._all_identifiers_cached and not self._is_expired(self._all_identifiers_cached[0]):
            return self._all_identifiers_cached[1]

        identifiers = self._provider.list_identifiers()
        self._all_identifiers_cached = (now, identifiers)
        return identifiers

    def load_all(self) -> Sequence[GovernanceContext]:
        now = time.monotonic()
        if self._all_cached and not self._is_expired(self._all_cached[0]):
            return self._all_cached[1]

        contexts = self._provider.load_all()
        # Also populate individual cache
        for ctx in contexts:
            # Use the institutional identifier (assuming every GovernanceContext has one)
            inst = ctx.institutional
            if inst and inst.identifier:
                self._cache[inst.identifier] = (now, ctx)
        self._all_cached = (now, contexts)
        return contexts
