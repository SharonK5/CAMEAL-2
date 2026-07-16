"""
===============================================================================
Module: query.execution.execution_context

Shared runtime context for execution stages.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ExecutionContext:
    """
    Shared execution state.

    Every stage reads from and writes to this object.
    """

    values: dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.values[key] = value

    # ------------------------------------------------------------------

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self.values.get(key, default)

    # ------------------------------------------------------------------

    def contains(
        self,
        key: str,
    ) -> bool:

        return key in self.values

    # ------------------------------------------------------------------

    def remove(
        self,
        key: str,
    ) -> None:

        self.values.pop(key, None)

    # ------------------------------------------------------------------

    def clear(self) -> None:

        self.values.clear()

    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:

        return dict(self.values)
