# security/policy/default_policy_provider.py
from __future__ import annotations

from typing import Tuple

from .policy_provider import PolicyRepositoryProvider
from .models import Policy, PolicyRequest


class DefaultPolicyProvider(PolicyRepositoryProvider):
    """
    Default in-memory policy provider.

    Returns a single default policy that always allows.
    """

    PROVIDER_NAME = "DefaultPolicyProvider"
    PROVIDER_VERSION = "1.0.0"

    def get_policies(self, request: PolicyRequest) -> Tuple[Policy, ...]:
        from .models import Policy, PolicyRule, PolicyEffect, PolicyVersion, PolicyType, PolicyStatus

        default_rule = PolicyRule(
            name="allow_all",
            effect=PolicyEffect.PERMIT,
            description="Allow all (default policy)",
        )
        default_policy = Policy(
            name="default_policy",
            policy_type=PolicyType.RULE,
            status=PolicyStatus.ACTIVE,
            version=PolicyVersion(1, 0, 0),
            rules=(default_rule,),
            description="Default policy that allows all requests.",
        )
        return (default_policy,)
