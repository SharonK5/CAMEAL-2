"""
===============================================================================
Module: query.execution.contracts.repository_result

Repository execution contract.
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence, Protocol, runtime_checkable

from .stage_result import StageResult


@runtime_checkable
class Repository(Protocol):
    """Minimal protocol for a repository."""
    @property
    def name(self) -> str:
        ...

    # Add other methods as needed (e.g., query, find, etc.)


@dataclass(slots=True, frozen=True)
class RepositoryResult(StageResult):
    """
    Immutable repository execution result.
    """

    repositories: Sequence[Repository] = ()
    count: int = 0

    def __post_init__(self) -> None:
        if self.count == 0 and self.repositories:
            object.__setattr__(self, "count", len(self.repositories))
