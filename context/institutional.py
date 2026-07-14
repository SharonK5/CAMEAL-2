"""
===============================================================================
Module: context.institutional

Institutional governance context.

Represents the governance actor responsible for, or participating in,
a decision, policy, workflow, document, or service.

The Institutional Context is intentionally independent of any specific
government, enterprise, or domain implementation.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True)
class InstitutionalContext:
    """
    Immutable institutional governance context.

    Represents an organization or governance actor within CAMEAL.
    """

    # -------------------------------------------------------------------------
    # Identity – identifier is now required
    # -------------------------------------------------------------------------
    identifier: str
    name: str | None = None
    institution_type: str | None = None

    # -------------------------------------------------------------------------
    # Governance
    # -------------------------------------------------------------------------
    sector: str | None = None
    level: str | None = None
    parent: str | None = None
    authority: str | None = None
    ownership: str | None = None

    # -------------------------------------------------------------------------
    # Governance Responsibilities
    # -------------------------------------------------------------------------
    mandates: tuple[str, ...] = ()
    responsibilities: tuple[str, ...] = ()

    # -------------------------------------------------------------------------
    # Additional Metadata – now hashable (tuple of key-value pairs)
    # -------------------------------------------------------------------------
    metadata: tuple[tuple[str, Any], ...] = ()

    def __post_init__(self) -> None:
        """Lightweight validation to keep the actor meaningful."""
        if not self.identifier.strip():
            raise ValueError("identifier cannot be empty or whitespace")
        if self.name is not None and not self.name.strip():
            raise ValueError("name cannot be empty if provided")
        if self.parent == self.identifier:
            raise ValueError("parent cannot reference self")

    # -------------------------------------------------------------------------
    # Convenience Methods
    # -------------------------------------------------------------------------
    def get(self, key: str, default: Any = None) -> Any:
        """Return a metadata value."""
        for k, v in self.metadata:
            if k == key:
                return v
        return default

    def contains(self, key: str) -> bool:
        """Return True if metadata contains the given key."""
        return any(k == key for k, _ in self.metadata)

    # -------------------------------------------------------------------------
    # Serialization (YAML round‑tripping)
    # -------------------------------------------------------------------------
    def to_dict(self) -> dict[str, Any]:
        """Convert to a dict suitable for YAML serialization."""
        return {
            "identifier": self.identifier,
            "name": self.name,
            "institution_type": self.institution_type,
            "sector": self.sector,
            "level": self.level,
            "parent": self.parent,
            "authority": self.authority,
            "ownership": self.ownership,
            "mandates": list(self.mandates),
            "responsibilities": list(self.responsibilities),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> InstitutionalContext:
        """Create an instance from a dict (e.g., loaded from YAML)."""
        data_copy = data.copy()
        for field_name in ("mandates", "responsibilities"):
            if field_name in data_copy and isinstance(data_copy[field_name], list):
                data_copy[field_name] = tuple(data_copy[field_name])
        if "metadata" in data_copy and isinstance(data_copy["metadata"], dict):
            data_copy["metadata"] = tuple(data_copy["metadata"].items())
        return cls(**data_copy)
