"""
===============================================================================
Module: repository.repository_validator

Repository Validator.

Validates Repository implementations.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from .repository import Repository


class RepositoryValidator:
    """
    Validates repository implementations.

    This validator ensures that a repository satisfies the
    minimum contract required by the CAMEAL Repository layer.
    """

    def validate(
        self,
        repository: Repository,
    ) -> None:
        """
        Validate a repository.

        Raises
        ------
        TypeError
            If the object is not a Repository.

        ValueError
            If required metadata is missing.
        """

        if not isinstance(repository, Repository):
            raise TypeError(
                "Expected Repository instance."
            )

        if not repository.name.strip():
            raise ValueError(
                "Repository name cannot be empty."
            )

        if not repository.version.strip():
            raise ValueError(
                "Repository version cannot be empty."
            )

    def is_valid(
        self,
        repository: Repository,
    ) -> bool:
        """
        Return True if the repository is valid.
        """

        try:
            self.validate(repository)
            return True
        except (TypeError, ValueError):
            return False
