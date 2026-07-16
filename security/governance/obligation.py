"""
===============================================================================
Module: security.obligation

Immutable governance obligation.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True)
class Obligation:
    """
    Immutable governance obligation.

    An obligation represents an action that must be executed after a
    governance decision.
    """

    obligation_id: str

    name: str

    description: str

    obligation_type: str

    parameters: dict[str, Any] = field(default_factory=dict)

    enabled: bool = True
