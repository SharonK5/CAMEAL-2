"""
===============================================================================
Module: repository.repository

Canonical Repository Interface.

Defines the abstract contract for all CAMEAL repositories.

A Repository manages immutable governance assets independently of
their underlying storage technology.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Iterable


class Repository(ABC):
    """
    Abstract governance repository.

    A Repository provides deterministic access to governance assets
    regardless of how or where they are stored.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Human-readable repository name.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def version(self) -> str:
        """
        Repository version.
        """
        raise NotImplementedError

    @abstractmethod
    def contains(
        self,
        identifier: str,
    ) -> bool:
        """
        Return True if an asset exists.
        """
        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        identifier: str,
    ) -> Any:
        """
        Retrieve an asset by identifier.

        Raises
        ------
        KeyError
            If the asset does not exist.
        """
        raise NotImplementedError

    @abstractmethod
    def list(
        self,
    ) -> Iterable[str]:
        """
        Return all registered asset identifiers.
        """
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        query: str,
    ) -> Iterable[Any]:
        """
        Search the repository.

        Implementations determine how searching is performed.
        """
        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        asset: Any,
    ) -> None:
        """
        Register a governance asset.
        """
        raise NotImplementedError

    @abstractmethod
    def unregister(
        self,
        identifier: str,
    ) -> None:
        """
        Remove an asset.
        """
        raise NotImplementedError

    @abstractmethod
    def clear(
        self,
    ) -> None:
        """
        Remove all assets.
        """
        raise NotImplementedError

    @abstractmethod
    def size(
        self,
    ) -> int:
        """
        Return the number of registered assets.
        """
        raise NotImplementedError
