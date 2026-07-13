"""
===============================================================================
Module: security.decision

Immutable authorization decision.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(slots=True, frozen=True)
class Decision:
    """
    Final governance decision.
    """

    permitted: bool

    reason: str

    policy_id: str | None = None

    evaluator: str = "PolicyEngine"

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
