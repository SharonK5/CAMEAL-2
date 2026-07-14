"""
===============================================================================
Module: security.risk_engine

Deterministic governance risk classification.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from .authorization_request import AuthorizationRequest
from .context import Context
from .policy import Policy
from .risk_level import RiskLevel


class RiskEngine:
    """
    Deterministic governance risk engine.
    """

    def classify(
        self,
        request: AuthorizationRequest,
        policy: Policy | None,
        context: Context,
    ) -> RiskLevel:
        """
        Determine the governance risk for an authorization request.
        """

        # Missing policy always increases uncertainty.
        if policy is None:
            return RiskLevel.HIGH

        # Administrative permissions are inherently high risk.
        if request.permission.value == "admin":
            return RiskLevel.CRITICAL

        # Governance actions deserve elevated scrutiny.
        if request.permission.value == "govern":
            return RiskLevel.HIGH

        # Sensitive contexts increase risk.
        if getattr(context, "sensitivity", "").lower() == "high":
            return RiskLevel.HIGH

        # Default.
        return RiskLevel.LOW
