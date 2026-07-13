"""
===============================================================================
Module: security.decision_engine

Governance Decision Engine.

Coordinates authorization and policy evaluation to produce a
single immutable Decision.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from typing import Protocol

from .authorization_request import AuthorizationRequest
from .authorizer import Authorizer
from .decision import Decision
from .policy import Policy  # assuming Policy is defined in .policy_engine or similar


class PolicyEvaluator(Protocol):
    """Protocol for any policy evaluation component."""

    def evaluate(self, request: AuthorizationRequest) -> Policy | None:
        """
        Evaluate the given request against available policies.

        Returns:
            The matching Policy if found, otherwise None.
        """
        ...


class DecisionEngine:
    """
    Coordinates governance decisions.

    The engine is decoupled from concrete implementations of both
    authorization and policy evaluation via dependency injection.
    """

    def __init__(
        self,
        authorizer: Authorizer,
        evaluator: PolicyEvaluator,  # <-- now uses the protocol
    ) -> None:
        self._authorizer = authorizer
        self._evaluator = evaluator

    def evaluate(self, request: AuthorizationRequest) -> Decision:
        authorization = self._authorizer.authorize(request)

        if not authorization.success:
            return Decision(
                permitted=False,
                reason=authorization.message,
            )

        policy = self._evaluator.evaluate(request)

        if policy is None:
            return Decision(
                permitted=False,
                reason="No matching policy.",
            )

        return Decision(
            permitted=True,
            reason="Policy matched.",
            policy_id=policy.policy_id,
        )
