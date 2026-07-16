"""
===============================================================================
Module: security.constraint

Immutable governance constraint definition.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True)
class Constraint:
    """
    Immutable governance constraint.

    A constraint describes a condition that must be evaluated by the
    ConstraintEngine. It contains no evaluation logic itself.
    """

    constraint_id: str

    name: str

    description: str

    constraint_type: str

    parameters: dict[str, Any] = field(default_factory=dict)

    enabled: bool = True
