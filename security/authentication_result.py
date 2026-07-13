"""
===============================================================================
Module: security.authentication_result

Immutable authentication result.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from .user import User


@dataclass(slots=True, frozen=True)
class AuthenticationResult:
    """
    Immutable authentication result.
    """

    success: bool

    user: User | None = None

    message: str = ""

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
