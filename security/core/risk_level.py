"""
===============================================================================
Module: security.risk_level

Risk classification levels used throughout CAMEAL governance.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from enum import IntEnum


class RiskLevel(IntEnum):
    """
    Standard governance risk levels.

    Ordered from lowest to highest risk.
    """

    LOW = 1

    MODERATE = 2

    HIGH = 3

    CRITICAL = 4

    def higher_than(
        self,
        other: "RiskLevel",
    ) -> bool:
        """
        Return True if this risk is higher.
        """
        return self > other

    def at_least(
        self,
        other: "RiskLevel",
    ) -> bool:
        """
        Return True if this risk is at least the supplied level.
        """
        return self >= other
