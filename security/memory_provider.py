"""
===============================================================================
Module: security.memory_provider

In-memory identity provider.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from .identity_provider import IdentityProvider
from .identity_record import IdentityRecord


class MemoryIdentityProvider(IdentityProvider):
    """
    In-memory implementation.
    """

    def __init__(self) -> None:

        self._users: dict[str, IdentityRecord] = {}

    def get(
        self,
        username: str,
    ) -> IdentityRecord | None:

        return self._users.get(username)

    def save(
        self,
        identity: IdentityRecord,
    ) -> None:

        self._users[
            identity.user.username
        ] = identity

    def exists(
        self,
        username: str,
    ) -> bool:

        return username in self._users
