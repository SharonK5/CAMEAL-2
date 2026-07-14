"""
===============================================================================
Module: context.context

Canonical CAMEAL Context.

Provides the immutable operational context shared across the CAMEAL
framework. The context captures the dimensions that influence
governance, adaptation, monitoring, evaluation, accountability,
learning, and decision-making.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Mapping


@dataclass(slots=True, frozen=True)
class GovernanceContext:
    """
    Immutable CAMEAL governance context.

    The context captures four primary dimensions:

    - Institutional
    - Jurisdictional
    - Spatial
    - Temporal

    Additional metadata may be attached without modifying the class.
    """

    # ------------------------------------------------------------------
    # Institutional Dimension
    # ------------------------------------------------------------------

    institution: str | None = None

    department: str | None = None

    programme: str | None = None

    # ------------------------------------------------------------------
    # Jurisdictional Dimension
    # ------------------------------------------------------------------

    jurisdiction: str | None = None

    policy_domain: str | None = None

    legal_framework: str | None = None

    # ------------------------------------------------------------------
    # Spatial Dimension
    # ------------------------------------------------------------------

    location: str | None = None

    region: str | None = None

    country: str | None = None

    # ------------------------------------------------------------------
    # Temporal Dimension
    # ------------------------------------------------------------------

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    period: str | None = None

    # ------------------------------------------------------------------
    # Operational Context
    # ------------------------------------------------------------------

    workflow: str | None = None

    environment: str | None = None

    emergency: bool = False

    # ------------------------------------------------------------------
    # Extension Metadata
    # ------------------------------------------------------------------

    metadata: Mapping[str, Any] = field(
        default_factory=dict
    )

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Return a metadata value.
        """
        return self.metadata.get(key, default)

    def contains(
        self,
        key: str,
    ) -> bool:
        """
        Return True if metadata contains the given key.
        """
        return key in self.metadata
