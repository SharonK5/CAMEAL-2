"""
===============================================================================
Module: services.analytics.analytics_result

Analytics Result.

Represents the output produced by an analytics service.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class AnalyticsResult:
    """
    Result produced by an analytics service.
    """

    success: bool

    summary: str

    findings: tuple[Any, ...] = ()

    confidence: float = 1.0

    metadata: tuple[tuple[str, Any], ...] = ()
