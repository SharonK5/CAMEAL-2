"""
===============================================================================
Module: context.context

Canonical CAMEAL Governance Context.

Represents the complete governance context by composing the individual
context dimensions used throughout the CAMEAL framework.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .institutional import InstitutionalContext
from .jurisdictional import JurisdictionalContext
from .spatial import SpatialContext
from .temporal import TemporalContext
from .operational import OperationalContext


@dataclass(slots=True, frozen=True)
class GovernanceContext:
    """
    Canonical CAMEAL governance context.

    A GovernanceContext is composed from the five governance dimensions.

    Institutional  -> Who is responsible?
    Jurisdictional -> Under whose authority?
    Spatial        -> Where?
    Temporal       -> When?
    Operational    -> Under what operating conditions?
    """

    institutional: InstitutionalContext | None = None
    jurisdictional: JurisdictionalContext | None = None
    spatial: SpatialContext | None = None
    temporal: TemporalContext | None = None
    operational: OperationalContext | None = None

    # metadata is now a tuple of (key, value) pairs – hashable
    metadata: tuple[tuple[str, Any], ...] = ()

    def get(self, key: str, default: Any = None) -> Any:
        """Return metadata value."""
        for k, v in self.metadata:
            if k == key:
                return v
        return default

    def contains(self, key: str) -> bool:
        """Return True if metadata contains key."""
        return any(k == key for k, _ in self.metadata)
