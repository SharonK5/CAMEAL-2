"""
===============================================================================
Module: context.temporal

Temporal governance context.

Represents the temporal environment associated with governance
decisions, policies, workflows, documents, monitoring, evaluation,
learning, and accountability.

The Temporal Context intentionally remains independent of any specific
calendar, scheduling, or workflow implementation.

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
class TemporalContext:
    """
    Immutable temporal governance context.
    """

    # -------------------------------------------------------------------------
    # Identity
    # -------------------------------------------------------------------------

    identifier: str | None = None

    name: str | None = None

    # -------------------------------------------------------------------------
    # Time
    # -------------------------------------------------------------------------

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    start_time: datetime | None = None

    end_time: datetime | None = None

    # -------------------------------------------------------------------------
    # Governance Time
    # -------------------------------------------------------------------------

    reporting_period: str | None = None

    fiscal_year: str | None = None

    financial_quarter: str | None = None

    season: str | None = None

    # Examples:
    # Long Rains
    # Short Rains
    # Dry Season
    # Wet Season

    phase: str | None = None

    # Examples:
    # Planning
    # Monitoring
    # Evaluation
    # Learning
    # Accountability

    # -------------------------------------------------------------------------
    # Versioning
    # -------------------------------------------------------------------------

    version: str | None = None

    revision: int = 1

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
