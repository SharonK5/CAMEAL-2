"""
===============================================================================
Module: query.query_registry

Registry for Query definitions.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from .query import Query


class QueryRegistry:
    """
    Registry of immutable Query objects.

    Responsible only for registration and lookup.
    """

    def __init__(self) -> None:

        self._queries: dict[str, Query] = {}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(
        self,
        identifier: str,
        query: Query,
    ) -> None:
        """
        Register a query.

        Raises
        ------
        KeyError
            If identifier already exists.
        """

        if identifier in self._queries:
            raise KeyError(
                f"Query '{identifier}' is already registered."
            )

        self._queries[identifier] = query

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    def get(
        self,
        identifier: str,
    ) -> Query | None:
        """
        Return a registered query.
        """

        return self._queries.get(identifier)

    # ------------------------------------------------------------------
    # Membership
    # ------------------------------------------------------------------

    def contains(
        self,
        identifier: str,
    ) -> bool:

        return identifier in self._queries

    # ------------------------------------------------------------------
    # Removal
    # ------------------------------------------------------------------

    def unregister(
        self,
        identifier: str,
    ) -> None:

        self._queries.pop(identifier, None)

    # ------------------------------------------------------------------
    # Collection
    # ------------------------------------------------------------------

    def identifiers(
        self,
    ) -> tuple[str, ...]:

        return tuple(sorted(self._queries.keys()))

    def queries(
        self,
    ) -> tuple[Query, ...]:

        return tuple(self._queries.values())

    def clear(
        self,
    ) -> None:

        self._queries.clear()

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------

    def __contains__(
        self,
        identifier: str,
    ) -> bool:

        return self.contains(identifier)

    def __len__(
        self,
    ) -> int:

        return len(self._queries)

    def __iter__(
        self,
    ):

        return iter(self._queries.values())
