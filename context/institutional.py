"""
===============================================================================
Module: context.institutional

Institutional governance context.

Represents the governance actor responsible for, or participating in,
a decision, policy, workflow, document, or service.

The Institutional Context is intentionally independent of any specific
government, enterprise, or domain implementation.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(slots=True, frozen=True)
class InstitutionalContext:
    """
    Immutable institutional governance context.

    Represents an organization or governance actor within CAMEAL.
    """

    # -------------------------------------------------------------------------
    # Identity
    # -------------------------------------------------------------------------

    identifier: str | None = None

    name: str | None = None

    institution_type: str | None = None

    # Examples:
    # Government
    # Ministry
    # County
    # NGO
    # University
    # Cooperative
    # Enterprise
    # Research Institute

    # -------------------------------------------------------------------------
    # Governance
    # -------------------------------------------------------------------------

    sector: str | None = None

    level: str | None = None

    # Examples:
    # International
    # National
    # Regional
    # County
    # Local
    # Department
    # Unit

    parent: str | None = None

    authority: str | None = None

    # Examples:
    # Strategic
    # Regulatory
    # Operational
    # Advisory

    ownership: str | None = None

    # Examples:
    # Public
    # Private
    # Community
    # Multilateral
    # Hybrid

    # -------------------------------------------------------------------------
    # Governance Responsibilities
    # -------------------------------------------------------------------------

    mandates: tuple[str, ...] = ()

    responsibilities: tuple[str, ...] = ()

    # -------------------------------------------------------------------------
    # Additional Metadata
    # -------------------------------------------------------------------------

    metadata: Mapping[str, Any] = field(
        default_factory=dict
    )

    # -------------------------------------------------------------------------
    # Convenience Methods
    # -------------------------------------------------------------------------

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
