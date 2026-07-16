"""
===============================================================================
Module: security.audit

Immutable audit events.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


@dataclass(slots=True, frozen=True)
class AuditEvent:
    """
    Immutable audit event.
    """

    action: str

    user: str | None = None

    session: str | None = None

    resource: str | None = None

    success: bool = True

    metadata: dict[str, Any] = field(default_factory=dict)

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    event_id: str = field(
        default_factory=lambda: str(uuid4())
    )
