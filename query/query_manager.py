"""
===============================================================================
Module: query.query_manager

Lifecycle manager for QueryRequest objects.

The QueryManager is responsible for managing registered QueryRequest definitions.
It does not execute queries; execution is delegated to the QueryEngine.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from .query_registry import QueryRegistry
from .query_request import QueryRequest   # changed import


class QueryManager:
    """
    Manages the lifecycle of QueryRequest definitions.
    """

    def __init__(
        self,
        registry: QueryRegistry | None = None,
    ) -> None:
        self._registry = registry or QueryRegistry()

    @property
    def registry(self) -> QueryRegistry:
        """
        Read-only access to the underlying registry.
        """
        return self._registry

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(
        self,
        query: QueryRequest,          # changed type hint
    ) -> None:
        """
        Register a query definition.
        """
        self._registry.register(query.identifier, query)   # pass identifier

    def unregister(
        self,
        identifier: str,
    ) -> None:
        """
        Remove a query definition.
        """
        self._registry.unregister(identifier)

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get(
        self,
        identifier: str,
    ) -> QueryRequest | None:        # changed return type
        """
        Retrieve a registered query.
        """
        return self._registry.get(identifier)

    def contains(
        self,
        identifier: str,
    ) -> bool:
        """
        Determine whether a query is registered.
        """
        return self._registry.contains(identifier)

    # ------------------------------------------------------------------
    # Enumeration
    # ------------------------------------------------------------------

    def queries(self) -> tuple[QueryRequest, ...]:   # changed return type
        """
        Return all registered queries.
        """
        return self._registry.queries()

    def identifiers(self) -> tuple[str, ...]:
        """
        Return all registered identifiers.
        """
        return self._registry.identifiers()

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------

    def clear(self) -> None:
        """
        Remove every registered query.
        """
        self._registry.clear()

    def count(self) -> int:
        """
        Number of registered queries.
        """
        return len(self._registry)
