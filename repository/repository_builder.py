"""
===============================================================================
Module: repository.repository_builder

Repository Builder.

Constructs validated Repository instances.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from .repository import Repository
from .repository_provider import RepositoryProvider
from .repository_validator import RepositoryValidator


class RepositoryBuilder:
    """
    Builds Repository instances.

    A RepositoryBuilder assembles a repository with its storage provider
    and validates the final configuration before returning it.
    """

    def __init__(self) -> None:

        self._repository: Repository | None = None
        self._provider: RepositoryProvider | None = None
        self._validator = RepositoryValidator()

    def repository(
        self,
        repository: Repository,
    ) -> "RepositoryBuilder":
        """
        Set the repository.
        """

        self._repository = repository
        return self

    def provider(
        self,
        provider: RepositoryProvider,
    ) -> "RepositoryBuilder":
        """
        Set the repository provider.
        """

        self._provider = provider
        return self

    def build(self) -> Repository:
        """
        Build a validated repository.

        Raises
        ------
        ValueError
            If a repository has not been supplied.
        """

        if self._repository is None:
            raise ValueError(
                "Repository has not been configured."
            )

        # Attach provider if repository supports it.
        if (
            self._provider is not None
            and hasattr(self._repository, "provider")
        ):
            setattr(
                self._repository,
                "provider",
                self._provider,
            )

        self._validator.validate(
            self._repository,
        )

        return self._repository
