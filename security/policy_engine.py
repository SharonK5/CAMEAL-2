"""
===============================================================================
Module: security.policy_engine

Policy evaluation engine.

Responsibilities
----------------
- Evaluate immutable policies.
- Determine whether a policy authorizes a request.
- Remain deterministic and stateless.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

from .permissions import Permission
from .policy import Policy
from .roles import Role


class PolicyEngine:
    """
    Stateless policy evaluator.
    """

    def evaluate(
        self,
        policy: Policy,
        role: Role,
        permission: Permission,
    ) -> bool:
        """
        Evaluate a policy.

        Returns
        -------
        bool
            True if the policy authorizes the requested permission.
        """

        if not policy.enabled:
            return False

        if not policy.allows_role(role):
            return False

        if not policy.allows_permission(permission):
            return False

        return True
