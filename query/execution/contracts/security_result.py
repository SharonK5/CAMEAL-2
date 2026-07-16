from __future__ import annotations

"""
===============================================================================
Module: query.execution.contracts.security_result

Security execution contract.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from dataclasses import dataclass
from typing import Any

from .stage_result import StageResult


@dataclass(slots=True, frozen=True)
class SecurityResult(StageResult):
    """
    Immutable security execution result.
    """

    allowed: bool = False
    decision: Any | None = None
    risk_level: str | None = None
    obligations: tuple[Any, ...] = ()
    constraints: tuple[Any, ...] = ()
    audit_identifier: str | None = None

    @property
    def denied(self) -> bool:
        return not self.allowed

    def to_dict(self) -> dict[str, Any]:
        # Explicitly call parent method to avoid super() issues
        data = StageResult.to_dict(self)
        data.update({
            "allowed": self.allowed,
            "risk_level": self.risk_level,
            "audit_identifier": self.audit_identifier,
        })
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SecurityResult":
        data = data.copy()
        if "metadata" in data:
            data["metadata"] = tuple(data["metadata"].items())
        return cls(**data)
