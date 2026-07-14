"""
===============================================================================
Module: context.operational

Operational governance context.

Represents the operational environment in which governance decisions,
policies, workflows, monitoring activities, and AI services execute.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(slots=True, frozen=True)
class OperationalContext:
    """
    Immutable operational governance context.
    """

    # -------------------------------------------------------------------------
    # Identity
    # -------------------------------------------------------------------------

    identifier: str | None = None

    name: str | None = None

    # -------------------------------------------------------------------------
    # Operating Environment
    # -------------------------------------------------------------------------

    environment: str | None = None

    # Development
    # Testing
    # Staging
    # Production

    workflow: str | None = None

    workflow_stage: str | None = None

    process: str | None = None

    service: str | None = None

    operation: str | None = None

    # -------------------------------------------------------------------------
    # Technology
    # -------------------------------------------------------------------------

    platform: str | None = None

    technology: str | None = None

    execution_mode: str | None = None

    # Human
    # AI
    # Human-AI
    # Autonomous

    # -------------------------------------------------------------------------
    # Operating State
    # -------------------------------------------------------------------------

    status: str | None = None

    priority: str | None = None

    emergency: bool = False

    automated: bool = False

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
        Return metadata value.
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
