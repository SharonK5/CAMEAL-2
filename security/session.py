"""
===============================================================================
Module: security.session

Authenticated session.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from uuid import uuid4


@dataclass(slots=True)
class Session:
    """
    Authenticated user session.
    """

    session_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    username: str = ""

    created: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    expires: datetime = field(
        default_factory=lambda: datetime.now(UTC) + timedelta(hours=8)
    )

    active: bool = True

    last_activity: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    def is_expired(self) -> bool:
        return datetime.now(UTC) >= self.expires

    def touch(self) -> None:
        self.last_activity = datetime.now(UTC)
