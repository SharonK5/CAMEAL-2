"""
===============================================================================
Module: security.identity_provider

Abstract identity provider.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .identity_record import IdentityRecord


class IdentityProvider(ABC):
    """
    Abstract identity provider.
    """

    @abstractmethod
    def get(
        self,
        username: str,
    ) -> IdentityRecord | None:
        """
        Return an identity or None.
        """

    @abstractmethod
    def save(
        self,
        identity: IdentityRecord,
    ) -> None:
        """
        Persist an identity.
        """

    @abstractmethod
    def exists(
        self,
        username: str,
    ) -> bool:
        """
        Check if an identity exists.
        """
