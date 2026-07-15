"""
===============================================================================
Module: repository.repository_factory

Repository Factory.

Creates Repository instances from registered repository classes.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from typing import Callable

from .repository import Repository


class RepositoryFactory:
    """
    Repository factory.

    Maintains a registry of repository constructors.
    """

    def __init__(self) -> None:

        self._constructors: dict[
            str,
            Callable[[], Repository],
        ] = {}

    def register(
        self,
        repository_type: str,
        constructor: Callable[[], Repository],
    ) -> None:
        """
        Register a repository constructor.
        """

        if repository_type in self._constructors:
            raise ValueError(
                f"Repository type '{repository_type}' already registered."
            )

        self._constructors[
            repository_type
        ] = constructor

    def unregister(
        self,
        repository_type: str,
    ) -> None:

        del self._constructors[
            repository_type
        ]

    def create(
        self,
        repository_type: str,
    ) -> Repository:
        """
        Create a repository.

        Raises
        ------
        KeyError
            Unknown repository type.
        """

        try:
            constructor = self._constructors[
                repository_type
            ]
        except KeyError as exc:
            raise KeyError(
                f"Unknown repository type '{repository_type}'."
            ) from exc

        return constructor()

    def contains(
        self,
        repository_type: str,
    ) -> bool:

        return repository_type in self._constructors

    def repository_types(
        self,
    ) -> tuple[str, ...]:

        return tuple(
            sorted(
                self._constructors.keys()
            )
        )

    def clear(
        self,
    ) -> None:

        self._constructors.clear()

    def size(
        self,
    ) -> int:

        return len(self._constructors)
