"""
===============================================================================
Module: query.execution.contracts.stage_result

Base contract for execution stage results.

Every execution stage returns an immutable StageResult-derived object.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class StageResult:
    """
    Base result returned by every execution stage.
    """

    success: bool

    stage: str

    metadata: tuple[tuple[str, Any], ...] = ()

    # ------------------------------------------------------------------
    # Metadata helpers
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

        for k, value in self.metadata:

            if k == key:
                return value

        return default

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:

        return {
            "success": self.success,
            "stage": self.stage,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "StageResult":

        data = data.copy()

        if "metadata" in data:

            data["metadata"] = tuple(
                data["metadata"].items()
            )

        return cls(**data)
