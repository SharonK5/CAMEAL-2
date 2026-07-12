"""
===============================================================================
Module: kernel.route

Immutable routing object.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Route:
    """
    Immutable route configuration.
    """

    action: str

    component: str

    workflow: str | None = None

    priority: int = 100

    authentication: bool = False

    governance: bool = False
