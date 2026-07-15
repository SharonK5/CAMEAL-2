"""
===============================================================================
Module: query.query_builder

Fluent builder for constructing immutable QueryRequest objects.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from typing import Any

from context.context import GovernanceContext
from context.context_registry import ContextRegistry
from context.context_resolver import ContextResolver
from .query_intent import QueryIntent
from .query_request import QueryRequest


class QueryBuilder:
    """
    Fluent builder for QueryRequest.
    """

    def __init__(
        self,
        registry: ContextRegistry | None = None,
    ) -> None:
        self._registry = registry
        self._resolver = (
            ContextResolver(registry)
            if registry is not None
            else None
        )

        self._identifier: str | None = None
        self._intent: QueryIntent = QueryIntent.RETRIEVE   # default
        self._query: str | None = None
        self._source: str = "unknown"
        self._context: GovernanceContext | None = None
        self._repositories: list[str] = []
        self._parameters: list[tuple[str, Any]] = []
        self._metadata: list[tuple[str, Any]] = []
        self._priority: int = 0

    # ------------------------------------------------------------------
    # Required fields
    # ------------------------------------------------------------------

    def identifier(self, identifier: str) -> QueryBuilder:
        self._identifier = identifier
        return self

    def intent(self, intent: QueryIntent) -> QueryBuilder:
        self._intent = intent
        return self

    def query(self, query: str) -> QueryBuilder:
        self._query = query
        return self

    # ------------------------------------------------------------------
    # Optional fields
    # ------------------------------------------------------------------

    def source(self, source: str) -> QueryBuilder:
        self._source = source
        return self

    def context(self, context: GovernanceContext) -> QueryBuilder:
        """Set the governance context directly."""
        self._context = context
        return self

    def context_id(self, identifier: str) -> QueryBuilder:
        """
        Resolve a governance context by its identifier using the registry.
        """
        if self._resolver is None:
            raise RuntimeError(
                "No ContextRegistry supplied to QueryBuilder. "
                "Use context() directly or pass a registry to the constructor."
            )
        self._context = self._resolver.resolve(identifier)
        return self

    def repository(self, repository: str) -> QueryBuilder:
        self._repositories.append(repository)
        return self

    def parameter(self, key: str, value: Any) -> QueryBuilder:
        self._parameters.append((key, value))
        return self

    def metadata(self, key: str, value: Any) -> QueryBuilder:
        self._metadata.append((key, value))
        return self

    def priority(self, priority: int) -> QueryBuilder:
        self._priority = priority
        return self

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def build(self) -> QueryRequest:
        if self._identifier is None:
            raise ValueError("identifier is required")
        if self._query is None:
            raise ValueError("query is required")

        return QueryRequest(
            identifier=self._identifier,
            intent=self._intent,
            query=self._query,
            source=self._source,
            context=self._context,
            repositories=tuple(self._repositories),
            parameters=tuple(self._parameters),
            metadata=tuple(self._metadata),
            priority=self._priority,
        )
