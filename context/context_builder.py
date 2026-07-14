"""
===============================================================================
Module: context.context_builder

Builder for GovernanceContext.

Provides a fluent interface for composing immutable governance contexts
from the individual context dimensions.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from .context import GovernanceContext
from .institutional import InstitutionalContext
from .jurisdictional import JurisdictionalContext
from .spatial import SpatialContext
from .temporal import TemporalContext
from .operational import OperationalContext


class ContextBuilder:
    """
    Builder for GovernanceContext.
    """

    def __init__(self) -> None:
        self._institutional: InstitutionalContext | None = None
        self._jurisdictional: JurisdictionalContext | None = None
        self._spatial: SpatialContext | None = None
        self._temporal: TemporalContext | None = None
        self._operational: OperationalContext | None = None

    # ------------------------------------------------------------------
    # Fluent setters
    # ------------------------------------------------------------------

    def add_institutional(
        self,
        context: InstitutionalContext,
    ) -> "ContextBuilder":
        self._institutional = context
        return self

    def add_jurisdictional(
        self,
        context: JurisdictionalContext,
    ) -> "ContextBuilder":
        self._jurisdictional = context
        return self

    def add_spatial(
        self,
        context: SpatialContext,
    ) -> "ContextBuilder":
        self._spatial = context
        return self

    def add_temporal(
        self,
        context: TemporalContext,
    ) -> "ContextBuilder":
        self._temporal = context
        return self

    def add_operational(
        self,
        context: OperationalContext,
    ) -> "ContextBuilder":
        self._operational = context
        return self

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def build(self) -> GovernanceContext:
        """
        Build an immutable GovernanceContext.
        """

        return GovernanceContext(
            institutional=self._institutional,
            jurisdictional=self._jurisdictional,
            spatial=self._spatial,
            temporal=self._temporal,
            operational=self._operational,
        )
