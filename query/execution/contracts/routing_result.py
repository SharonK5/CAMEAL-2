"""
===============================================================================
Module: query.execution.contracts.routing_result

Routing execution contract.
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

from .stage_result import StageResult


@runtime_checkable
class QueryHandler(Protocol):
    """Protocol for a query handler."""
    def handle(self, request) -> Any:
        ...


@dataclass(slots=True, frozen=True)
class RoutingResult(StageResult):
    """
    Immutable routing execution result.
    """

    handler: QueryHandler | None = None
    handler_name: str | None = None
