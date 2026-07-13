"""
===============================================================================
Module: security.user

Immutable user identity.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import FrozenSet
from uuid import uuid4

from .roles import Role


@dataclass(slots=True, frozen=True)
class User:
    """
    Immutable authenticated user.
    """

    username: str

    roles: FrozenSet[Role] = field(default_factory=frozenset)

    active: bool = True

    created: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    user_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    email: str | None = None

    display_name: str | None = None

    def has_role(self, role: Role) -> bool:
        """
        Return True if the user has the given role.
        """
        return role in self.roles
