"""
===============================================================================
Module: context.jurisdictional

Jurisdictional governance context.

Represents the legal, administrative, regulatory, or policy jurisdiction
under which governance decisions, workflows, documents, and services
operate.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(slots=True, frozen=True)
class JurisdictionalContext:
    """
    Immutable jurisdictional governance context.

    Represents the governing authority applicable to an activity,
    policy, document, workflow, or decision.
    """

    # -------------------------------------------------------------------------
    # Identity
    # -------------------------------------------------------------------------

    identifier: str | None = None

    name: str | None = None

    # -------------------------------------------------------------------------
    # Jurisdiction
    # -------------------------------------------------------------------------

    jurisdiction_type: str | None = None

    # Examples:
    # International
    # Regional
    # National
    # County
    # Municipal
    # Organizational
    # Project

    level: str | None = None

    parent: str | None = None

    code: str | None = None

    # ISO country code
    # County code
    # Administrative code

    # -------------------------------------------------------------------------
    # Governance
    # -------------------------------------------------------------------------

    authority: str | None = None

    # Examples:
    # Constitutional
    # Statutory
    # Regulatory
    # Administrative
    # Organizational

    legal_frameworks: tuple[str, ...] = ()

    policies: tuple[str, ...] = ()

    regulations: tuple[str, ...] = ()

    # -------------------------------------------------------------------------
    # Metadata
    # -------------------------------------------------------------------------

    metadata: Mapping[str, Any] = field(
        default_factory=dict
    )

    # -------------------------------------------------------------------------
    # Convenience
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
        Return True if metadata contains key.
        """
        return key in self.metadata
