"""
===============================================================================
Module: query.query_response

Immutable Query Response.

Represents the outcome of a CAMEAL query.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class QueryResponse:
    """
    Immutable query response.
    """

    identifier: str

    success: bool

    message: str = ""

    results: tuple[Any, ...] = ()

    repositories: tuple[str, ...] = ()

    metadata: tuple[tuple[str, Any], ...] = ()

    confidence: float = 1.0

    execution_time: float = 0.0

    def __post_init__(self) -> None:

        if not self.identifier.strip():
            raise ValueError(
                "identifier cannot be empty."
            )

        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(
                "confidence must be between 0.0 and 1.0."
            )

        if self.execution_time < 0:
            raise ValueError(
                "execution_time cannot be negative."
            )

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------

    def contains_metadata(
        self,
        key: str,
    ) -> bool:

        return any(
            k == key
            for k, _ in self.metadata
        )

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        for k, v in self.metadata:

            if k == key:
                return v

        return default

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:

        return {
            "identifier": self.identifier,
            "success": self.success,
            "message": self.message,
            "results": list(self.results),
            "repositories": list(self.repositories),
            "metadata": dict(self.metadata),
            "confidence": self.confidence,
            "execution_time": self.execution_time,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "QueryResponse":

        data = data.copy()

        if "results" in data:
            data["results"] = tuple(data["results"])

        if "repositories" in data:
            data["repositories"] = tuple(data["repositories"])

        if "metadata" in data:
            data["metadata"] = tuple(
                data["metadata"].items()
            )

        return cls(**data)
