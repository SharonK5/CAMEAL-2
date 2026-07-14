"""
===============================================================================
Module: context.context_builder

Builder for GovernanceContext.

Supports fluent and functional styles, with optional metadata validation.
===============================================================================
"""

from __future__ import annotations

from typing import Optional

from .context import GovernanceContext
from .institutional import InstitutionalContext
from .jurisdictional import JurisdictionalContext
from .spatial import SpatialContext
from .temporal import TemporalContext
from .operational import OperationalContext
from .metadata_validator import MetadataSchema


class ContextBuilder:
    def __init__(self):
        self._institutional: InstitutionalContext | None = None
        self._jurisdictional: JurisdictionalContext | None = None
        self._spatial: SpatialContext | None = None
        self._temporal: TemporalContext | None = None
        self._operational: OperationalContext | None = None

    # ------------------------------------------------------------------
    # Fluent setters (unchanged)
    # ------------------------------------------------------------------

    def add_institutional(self, context: InstitutionalContext) -> "ContextBuilder":
        self._institutional = context
        return self

    def add_jurisdictional(self, context: JurisdictionalContext) -> "ContextBuilder":
        self._jurisdictional = context
        return self

    def add_spatial(self, context: SpatialContext) -> "ContextBuilder":
        self._spatial = context
        return self

    def add_temporal(self, context: TemporalContext) -> "ContextBuilder":
        self._temporal = context
        return self

    def add_operational(self, context: OperationalContext) -> "ContextBuilder":
        self._operational = context
        return self

    # ------------------------------------------------------------------
    # Build with optional metadata validation
    # ------------------------------------------------------------------

    def build(
        self,
        institutional: InstitutionalContext | None = None,
        jurisdictional: JurisdictionalContext | None = None,
        spatial: SpatialContext | None = None,
        temporal: TemporalContext | None = None,
        operational: OperationalContext | None = None,
        metadata: tuple[tuple[str, object], ...] = (),
        metadata_schema: Optional[MetadataSchema] = None,
    ) -> GovernanceContext:
        """
        Build the GovernanceContext.

        If metadata_schema is provided, it validates the metadata tuple.
        Otherwise, no validation is performed (allows tests and flexible usage).
        """
        # Use provided kwargs, fallback to stored values
        final_institutional = institutional if institutional is not None else self._institutional
        final_jurisdictional = jurisdictional if jurisdictional is not None else self._jurisdictional
        final_spatial = spatial if spatial is not None else self._spatial
        final_temporal = temporal if temporal is not None else self._temporal
        final_operational = operational if operational is not None else self._operational

        # Validate only if a schema is explicitly given
        if metadata_schema is not None:
            metadata_schema.validate(metadata)

        return GovernanceContext(
            institutional=final_institutional,
            jurisdictional=final_jurisdictional,
            spatial=final_spatial,
            temporal=final_temporal,
            operational=final_operational,
            metadata=metadata,
        )
