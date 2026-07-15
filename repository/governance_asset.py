"""
===============================================================================
Module: repository.governance_asset

Base Governance Asset.

Defines the immutable base class for every governance asset
managed by the Repository.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Mapping


@dataclass(slots=True, frozen=True)
class GovernanceAsset(ABC):
    """
    Base governance asset.

    Every repository object derives from GovernanceAsset.
    """

    identifier: str

    name: str

    asset_type: str

    version: str = "1.0"

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    metadata: Mapping[str, Any] = field(
        default_factory=dict
    )

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        return self.metadata.get(key, default)

    def contains(
        self,
        key: str,
    ) -> bool:
        return key in self.metadata
