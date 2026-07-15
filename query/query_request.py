"""
===============================================================================
Module: query.query_request

Immutable Query Request.

Represents a request submitted to the CAMEAL Query Engine.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from context.context import GovernanceContext          # new import
from .query_intent import QueryIntent


@dataclass(slots=True, frozen=True)
class QueryRequest:
    """
    Immutable governance query request.
    """

    identifier: str
    intent: QueryIntent
    query: str
    source: str = "unknown"
    context: GovernanceContext | None = None           # changed from str
    repositories: tuple[str, ...] = ()
    parameters: tuple[tuple[str, Any], ...] = ()
    metadata: tuple[tuple[str, Any], ...] = ()
    priority: int = 0

    def __post_init__(self) -> None:
        if not self.identifier.strip():
            raise ValueError("identifier cannot be empty")
        if not self.query.strip():
            raise ValueError("query cannot be empty")

    # ------------------------------------------------------------------
    # Convenience Methods
    # ------------------------------------------------------------------

    def get_parameter(self, key: str, default: Any = None) -> Any:
        for k, v in self.parameters:
            if k == key:
                return v
        return default

    def get_metadata(self, key: str, default: Any = None) -> Any:
        for k, v in self.metadata:
            if k == key:
                return v
        return default

    def contains_parameter(self, key: str) -> bool:
        return any(k == key for k, _ in self.parameters)

    def contains_metadata(self, key: str) -> bool:
        return any(k == key for k, _ in self.metadata)

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        return {
            "identifier": self.identifier,
            "intent": self.intent.name,
            "query": self.query,
            "source": self.source,
            "context": (
                self.context.to_dict()
                if self.context is not None
                else None
            ),                                         # serialize full context
            "repositories": list(self.repositories),
            "parameters": dict(self.parameters),
            "metadata": dict(self.metadata),
            "priority": self.priority,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> QueryRequest:
        data = data.copy()
        data["intent"] = QueryIntent[data["intent"]]

        if data.get("context") is not None:
            data["context"] = GovernanceContext.from_dict(data["context"])

        if "repositories" in data:
            data["repositories"] = tuple(data["repositories"])
        if "parameters" in data:
            data["parameters"] = tuple(data["parameters"].items())
        if "metadata" in data:
            data["metadata"] = tuple(data["metadata"].items())

        return cls(**data)
