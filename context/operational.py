"""
===============================================================================
Module: context.operational

Operational governance context.

Defines the operational conditions under which a decision is made.
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(slots=True, frozen=True)
class OperationalContext:
    """
    Operational conditions of a governance action.
    """

    identifier: str | None = None
    name: str | None = None
    environment: str | None = None
    workflow: str | None = None
    workflow_stage: str | None = None
    process: str | None = None
    service: str | None = None
    operation: str | None = None
    platform: str | None = None
    technology: str | None = None
    execution_mode: str | None = None
    status: str | None = None
    priority: str | None = None
    emergency: bool = False
    automated: bool = False

    # Security‑critical field: classification of the operation
    sensitivity: str | None = None

    # Free‑form metadata (dict is fine – not used as a key)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    # Convenience methods (matching GovernanceContext)
    def get(self, key: str, default: Any = None) -> Any:
        return self.metadata.get(key, default)

    def contains(self, key: str) -> bool:
        return key in self.metadata
