"""
===============================================================================
Module: query.query_resolver

Query Resolver.

Resolves Query objects from the QueryRegistry.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from .query import Query
from .query_registry import QueryRegistry


class QueryResolver:
    """
    Resolves Query objects from a QueryRegistry.

    The resolver never creates Query objects.
    It only retrieves registered definitions.
    """

    def __init__(
        self,
        registry: QueryRegistry,
    ) -> None:

        self._registry = registry

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def registry(
        self,
    ) -> QueryRegistry:
        """
        Return the underlying registry (read-only).
        """

        return self._registry

    # ------------------------------------------------------------------
    # Resolution
    # ------------------------------------------------------------------

    def resolve(
        self,
        identifier: str,
    ) -> Query:
        """
        Resolve a registered Query.

        Raises
        ------
        KeyError
            If the Query does not exist.
        """

        query = self._registry.get(identifier)

        if query is None:

            raise KeyError(
                f"Unknown query '{identifier}'."
            )

        return query

    def resolve_many(
        self,
        identifiers: list[str] | tuple[str, ...],
    ) -> tuple[Query, ...]:
        """
        Resolve multiple registered queries.

        Raises
        ------
        KeyError
            If any identifier is unknown.
        """

        return tuple(
            self.resolve(identifier)
            for identifier in identifiers
        )

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------

    def exists(
        self,
        identifier: str,
    ) -> bool:
        """
        Return True if the Query exists.
        """

        return self._registry.contains(identifier)
