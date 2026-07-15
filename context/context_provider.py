"""
===============================================================================
Module: context.context_provider

Abstract interface for context providers.
===============================================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from .context import GovernanceContext


class ContextProvider(ABC):
    """
    Abstract provider of GovernanceContext objects.
    """

    @abstractmethod
    def get(self, identifier: str) -> GovernanceContext | None:
        """Retrieve a single context by identifier."""
        pass

    @abstractmethod
    def list_identifiers(self) -> Sequence[str]:
        """Return all known identifiers."""
        pass

    @abstractmethod
    def load_all(self) -> Sequence[GovernanceContext]:
        """Load all contexts (may be expensive)."""
        pass
