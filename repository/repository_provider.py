"""
===============================================================================
Module: repository.repository_provider

Canonical Repository Provider Interface.

Defines the storage abstraction used by Repository implementations.

Repository Providers are responsible for persisting and retrieving
governance assets from one or more storage technologies.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Iterable


class RepositoryProvider(ABC):
    """
    Abstract repository provider.

    Providers encapsulate the underlying storage implementation
    while exposing a deterministic interface to repositories.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Human-readable provider name.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def provider_type(self) -> str:
        """
        Provider technology.

        Examples
        --------
        yaml
        filesystem
        sqlite
        postgres
        neo4j
        vector
        api
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def connected(self) -> bool:
        """
        Return True if the provider is available.
        """
        raise NotImplementedError

    @abstractmethod
    def connect(self) -> None:
        """
        Establish a connection.
        """
        raise NotImplementedError

    @abstractmethod
    def disconnect(self) -> None:
        """
        Close the provider connection.
        """
        raise NotImplementedError

    @abstractmethod
    def exists(
        self,
        identifier: str,
    ) -> bool:
        """
        Return True if an asset exists.
        """
        raise NotImplementedError

    @abstractmethod
    def load(
        self,
        identifier: str,
    ) -> Any:
        """
        Load a governance asset.
        """
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        asset: Any,
    ) -> None:
        """
        Persist a governance asset.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        identifier: str,
    ) -> None:
        """
        Delete a governance asset.
        """
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        query: str,
    ) -> Iterable[Any]:
        """
        Search stored governance assets.
        """
        raise NotImplementedError

    @abstractmethod
    def identifiers(
        self,
    ) -> Iterable[str]:
        """
        Return all stored identifiers.
        """
        raise NotImplementedError
