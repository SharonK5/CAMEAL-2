"""
===============================================================================
Module: repository.repository_resolver

Repository Resolver.

Resolves Repository instances from the Repository Registry.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from .repository import Repository
from .repository_registry import RepositoryRegistry


class RepositoryResolver:
    """
    Resolves repositories from the registry.

    The resolver never creates repositories.
    It only retrieves registered repository instances.
    """

    def __init__(
        self,
        registry: RepositoryRegistry,
    ) -> None:

        self._registry = registry

    def resolve(
        self,
        identifier: str,
    ) -> Repository:
        """
        Resolve a repository.

        Raises
        ------
        KeyError
            If the repository does not exist.
        """

        repository = self._registry.get(identifier)

        if repository is None:
            raise KeyError(
                f"Unknown repository '{identifier}'."
            )

        return repository

    def exists(
        self,
        identifier: str,
    ) -> bool:
        """
        Return True if the repository exists.
        """

        return self._registry.contains(identifier)
