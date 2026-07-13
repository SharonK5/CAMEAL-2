"""
===============================================================================
Module: security.context

Immutable governance context.

Provides environmental information used when making governance
decisions. This class intentionally remains independent of any
specific security, AI, or workflow implementation.

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
    Immutable governance context.

    Captures the environment surrounding a governance decision.
    """

    jurisdiction: str | None = None

    institution: str | None = None

    workflow: str | None = None

    environment: str | None = None

    emergency: bool = False

    request_time: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

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
        Return True if metadata contains the key.
        """
        return key in self.metadata
