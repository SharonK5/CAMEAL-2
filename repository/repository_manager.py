"""
===============================================================================
Module: repository.repository_manager

Repository Manager.

Coordinates repository creation, validation, registration,
resolution, and lifecycle management.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from .repository import Repository
from .repository_factory import RepositoryFactory
from .repository_registry import RepositoryRegistry
from .repository_resolver import RepositoryResolver
from .repository_validator import RepositoryValidator


class RepositoryManager:
    """
    Coordinates repository infrastructure.

    The manager is the single orchestration point for repositories.
    """

    def __init__(
        self,
        factory: RepositoryFactory | None = None,
        registry: RepositoryRegistry | None = None,
        validator: RepositoryValidator | None = None,
    ) -> None:

        self._factory = factory or RepositoryFactory()
        self._registry = registry or RepositoryRegistry()
        self._validator = validator or RepositoryValidator()
        self._resolver = RepositoryResolver(self._registry)

    @property
    def factory(self) -> RepositoryFactory:
        return self._factory

    @property
    def registry(self) -> RepositoryRegistry:
        return self._registry

    @property
    def validator(self) -> RepositoryValidator:
        return self._validator

    @property
    def resolver(self) -> RepositoryResolver:
        return self._resolver

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(
        self,
        identifier: str,
        repository: Repository,
    ) -> None:

        self._validator.validate(repository)
        self._registry.register(
            identifier,
            repository,
        )

    def unregister(
        self,
        identifier: str,
    ) -> None:

        self._registry.unregister(identifier)

    # ------------------------------------------------------------------
    # Creation
    # ------------------------------------------------------------------

    def create(
        self,
        identifier: str,
        repository_type: str,
    ) -> Repository:
        """
        Create and register a repository.
        """

        repository = self._factory.create(
            repository_type,
        )

        self.register(
            identifier,
            repository,
        )

        return repository

    # ------------------------------------------------------------------
    # Resolution
    # ------------------------------------------------------------------

    def get(
        self,
        identifier: str,
    ) -> Repository:

        return self._resolver.resolve(
            identifier,
        )

    def contains(
        self,
        identifier: str,
    ) -> bool:

        return self._resolver.exists(
            identifier,
        )

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def identifiers(
        self,
    ) -> tuple[str, ...]:

        return self._registry.identifiers()

    def repositories(
        self,
    ) -> tuple[Repository, ...]:

        return self._registry.repositories()

    def clear(
        self,
    ) -> None:

        self._registry.clear()

    def size(
        self,
    ) -> int:

        return self._registry.size()
