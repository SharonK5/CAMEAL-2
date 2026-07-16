"""
===============================================================================
Module: security.identity_record

Authentication identity record.

Separates authentication state from the immutable User model.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from .user import User


@dataclass(slots=True)
class IdentityRecord:
    """
    Authentication identity record.
    """

    user: User

    password_hash: str

    enabled: bool = True

    locked: bool = False

    failed_attempts: int = 0

    created: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    last_login: datetime | None = None

    password_changed: datetime | None = None
