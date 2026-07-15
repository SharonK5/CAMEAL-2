"""
===============================================================================
Module: repository.repository_registry

Repository Registry.

Registers and manages Repository instances.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from typing import Dict, Iterable

from .repository import Repository


class RepositoryRegistry:
    """
    Registry of repositories.

    Maintains the available repositories within CAMEAL.
    """

    def __init__(self) -> None:
        self._repositories: Dict[str, Repository] = {}

    def register(
        self,
        identifier: str,
        repository: Repository,
    ) -> None:
        """
        Register a repository.

        Raises
        ------
        ValueError
            If identifier already exists.
        """
        if identifier in self._repositories:
            raise ValueError(
                f"Repository '{identifier}' already registered."
            )

        self._repositories[identifier] = repository

    def unregister(
        self,
        identifier: str,
    ) -> None:
        """
        Remove a repository.

        Raises
        ------
        KeyError
            If repository does not exist.
        """
        del self._repositories[identifier]

    def get(
        self,
        identifier: str,
    ) -> Repository | None:
        """
        Return a repository or None.
        """
        return self._repositories.get(identifier)

    def contains(
        self,
        identifier: str,
    ) -> bool:
        """
        Return True if repository exists.
        """
        return identifier in self._repositories

    def identifiers(self) -> tuple[str, ...]:
        """
        Return registered identifiers.
        """
        return tuple(sorted(self._repositories.keys()))

    def repositories(self) -> tuple[Repository, ...]:
        """
        Return registered repositories.
        """
        return tuple(self._repositories.values())

    def clear(self) -> None:
        """
        Remove every repository.
        """
        self._repositories.clear()

    def size(self) -> int:
        """
        Number of repositories.
        """
        return len(self._repositories)
