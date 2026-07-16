"""
===============================================================================
Module: security.authentication_request

Immutable authentication request.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(slots=True, frozen=True)
class AuthenticationRequest:
    """
    Immutable authentication request.
    """

    username: str

    password: str

    source: str = "unknown"

    remember_me: bool = False

    ip_address: str | None = None

    user_agent: str | None = None

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
