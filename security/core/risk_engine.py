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

from security.identity.authorization_request import AuthorizationRequest
from context.context import GovernanceContext
from security.governance.policy import Policy
from security.core.risk_level import RiskLevel


class RiskEngine:
    """
    Deterministic governance risk engine.
    """

    def classify(
        self,
        request: AuthorizationRequest,
        policy: Policy | None,
        context: GovernanceContext,   # fixed type hint
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
        # Read sensitivity from metadata (safe if missing).
        if str(context.get("sensitivity", "")).lower() == "high":
            return RiskLevel.HIGH

        # Default.
        return RiskLevel.LOW
